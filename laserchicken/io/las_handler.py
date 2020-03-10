""" IO Handler for LAS (and compressed LAZ) file format """
import pylas

from laserchicken import keys
from laserchicken.io.base_io_handler import IOHandler
from laserchicken.io.utils import convert_to_short_type, select_valid_attributes


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

    def read(self, attributes=DEFAULT_LAS_ATTRIBUTES):
        """
        Load the points from a LAS(LAZ) file into memory.

        :param attributes: list of attributes to read ('all' for all attributes in file)
        :return: point cloud data structure
        """
        file = pylas.read(self.path)
        attributes_available = [el if el not in ['X', 'Y', 'Z'] else el.lower()
                                for el in file.points.dtype.names]

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


def _get_attribute(data, data_type):
    return {'type': data_type, 'data': data}


def _get_data_and_type(attribute):
    return attribute['data'], attribute['type']
