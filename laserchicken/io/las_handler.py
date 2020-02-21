""" IO Handler for LAS (and compressed LAZ) file format """
from distutils.version import LooseVersion

from laserchicken import keys
from laserchicken.io.base_io_handler import IOHandler
from laserchicken.io.utils import convert_to_short_type, select_valid_attributes

is_pylas_available, is_lazperf_available = False, False
try:
    import pylas
    is_pylas_available = True
except ImportError:
    import laspy

try:
    import lazperf
    is_lazperf_available = True
except ImportError:
    pass

DEFAULT_LAS_ATTRIBUTES = {
    'x',
    'y',
    'z',
    'intensity',
    'gps_time',
    'raw_classification',
}


class LASHandler(IOHandler):
    """ Class for IO of point-cloud data in LAS file format """

    def __init__(self, path, mode, *args, **kwargs):
        if mode == 'w' and (not is_pylas_available):
            raise NotImplementedError('Writing LAS files only available through pylas: '
                                      'https://pylas.readthedocs.io')
        super(LASHandler, self).__init__(path, mode, *args, **kwargs)

    def read(self, attributes=DEFAULT_LAS_ATTRIBUTES):
        """
        Load the points from a LAS file into memory.

        :param attributes: list of attributes to read ('all' for all attributes in file)
        :return: point cloud data structure
        """
        if is_pylas_available:
            file = pylas.read(self.path)
            attributes_available = [el if el not in ['X', 'Y', 'Z'] else el.lower()
                                    for el in file.points.dtype.names]
        else:
            file = laspy.file.File(self.path)
            attributes_available = [el if el not in ['X', 'Y', 'Z'] else el.lower()
                                    for el in file.points.dtype['point'].names]

        attributes = select_valid_attributes(attributes_available, attributes)

        points = {}
        for name in attributes:
            if hasattr(file, name):
                data = getattr(file, name)
                points[name] = _get_attribute(data, data.dtype.name)

        return {keys.point: points}

    def write(self, point_cloud, attributes='all', file_version='1.2', point_format_id=3):
        """
        Write point cloud to a LAS(LAZ) file.

        :param point_cloud:
        :param attributes: list of attributes to write ('all' for all attributes in point_cloud)
        :param file_version:
        :param point_format_id:
        :return:
        """
        file = pylas.create(point_format_id=point_format_id,
                            file_version=file_version)

        points = point_cloud[keys.point]
        attributes = select_valid_attributes([attr for attr in points.keys()], attributes)

        # NOTE: adding extra dims and assignment should be done in two steps,
        # some fields (e.g. raw_classification) are otherwise overwritten
        for attribute in attributes:
            data, type = _get_data_and_type(points[attribute])
            type_short = convert_to_short_type(type)
            if attribute not in 'xyz':
                # x,y,z are not there but file methods can be used to convert coords to int4
                if attribute not in file.points.dtype.names:
                    file.add_extra_dim(name=attribute, type=type_short)
            file_type_short = convert_to_short_type(getattr(file, attribute).dtype.name)
            if not file_type_short == type_short:
                raise TypeError('Data type in file does not match the one in point cloud: '
                                'for {}, {} vs {}'.format(attribute, file_type_short, type_short))

        for attribute in attributes:
            data, _ = _get_data_and_type(points[attribute])
            if data.size == 0:
                raise ValueError('Cannot write empty point-cloud!')
            else:
                setattr(file, attribute, data)

        try:
            file.write(self.path)
        except ValueError as err:
            raise ValueError('Error in writing LAS file (file_version {}, point_format_id {}). '
                             'pylas error below:\n{}'.format(file_version, point_format_id, err))


class LAZHandler(LASHandler):
    """ Class for IO of point-cloud data in compressed LAZ file format """
    required_laspy_version = '1.7'

    def __init__(self, *args, **kwargs):
        if not is_lazperf_available:
            raise NotImplementedError('lazperf is required to read/write compressed LAZ files!')
        if not is_pylas_available:
            available_laspy_version = laspy.__version__
            if LooseVersion(available_laspy_version) < self.required_laspy_version:
                raise NotImplementedError('laspy version >= {} is required to deal with compressed LAZ files! '
                                          'available version: {}'.format(self.required_laspy_version,
                                                                         available_laspy_version))
        super(LAZHandler, self).__init__(*args, **kwargs)


def _get_attribute(data, data_type):
    return {'type': data_type, 'data': data}


def _get_data_and_type(attribute):
    return attribute['data'], attribute['type']
