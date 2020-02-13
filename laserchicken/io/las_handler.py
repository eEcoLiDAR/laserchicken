""" IO Handler for LAS (and compressed LAZ) file format """
import numpy as np

is_pylas_available = False
try:
    import pylas
    is_pylas_available = True
except ImportError:
    import laspy

from laserchicken import keys
from laserchicken.io.base_io_handler import IOHandler


class LASHandler(IOHandler):
    """ Class for IO of point-cloud data in LAS(LAZ) file format """

    def read(self):
        """
        Load the points from a LAS file into memory.

        :return: point cloud data structure
        """
        if is_pylas_available:
            file = pylas.read(self.path)
        else:
            file = laspy.file.File(self.path)

        attributes = {
            'x',
            'y',
            'z',
            'intensity',
            'gps_time',
            'raw_classification',
        }
        points = {}
        for name in attributes:
            if hasattr(file, name):
                data = getattr(file, name)
                points[name] = _get_attribute(data, data.dtype.name)

        return {keys.point: points}

    def write(self, point_cloud, file_version='1.4', point_format_id=1):
        """
        Write point cloud to a LAS(LAZ) file.

        :param point_cloud:
        :param file_version:
        :param point_format_id:
        :return:
        """
        if not is_pylas_available:
            raise NotImplementedError('Writing LAS/LAZ files only available through pylas: '
                                      'https://pylas.readthedocs.io')

        file = pylas.create(point_format_id=point_format_id,
                            file_version=file_version)

        points = point_cloud[keys.point]

        # NOTE: adding extra dims and assignment should be done in two steps,
        # some fields (e.g. raw_classification) are otherwise overwritten
        for name, attribute in points.items():
            data, dtype = _get_data_and_type(attribute)
            if name not in 'xyz':
                # x,y,z are not there but file methods can be used to convert coords to int4
                if name not in file.points.dtype.names:
                    dtype_str = "".join([c for c in dtype.str
                                         if c not in ['<', '>', '|']])
                    file.add_extra_dim(name=name, type=dtype_str)
            file_dtype = getattr(file, name).dtype
            if not file_dtype.name == dtype.name:
                raise TypeError('Open file format data type does not match point cloud: '
                                'for {}, {} vs {}'.format(name, file_dtype.name, dtype.name))

        for name, attribute in points.items():
            data, _ = _get_data_and_type(attribute)
            if data.size == 0:
                raise ValueError('Cannot write empty point-cloud!')
            else:
                setattr(file, name, data)

        file.write(self.path)


def _get_attribute(data, data_type):
    return {'type': data_type, 'data': data}


def _get_data_and_type(attribute):
    return attribute['data'], np.dtype(attribute['type'])


if __name__ == '__main__':
    from laserchicken import load, export
    from laserchicken.normalize import normalize
    pc = load('testdata/AHN3.las')
    normalize(pc)
    export(pc, 'testdata/tmp.las', overwrite=True)
