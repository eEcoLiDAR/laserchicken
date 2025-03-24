""" IO Handler for LAS (and compressed LAZ) file format """
import laspy
import numpy as np

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
        file = laspy.read(self.path)
        point_format = file.point_format
        # dimension_names gives access to all the standard and custom
        # dimensions, including derived sub-fields such as e.g.
        # "classification", "synthetic", "return_number", and
        # "number_of_returns")
        dim_names = list(point_format.dimension_names)
        # dtype gives access to "raw" dimensions packed as composed fields
        # (e.g. "raw_classification" and "bit_fields")
        raw_dim_names = list(point_format.dtype().fields.keys())
        attributes_available = [el if el not in ['X', 'Y', 'Z'] else el.lower()
                                for el in set(dim_names + raw_dim_names)]

        attributes = select_valid_attributes(attributes_available, attributes)

        points = {}
        for name in attributes:
            if hasattr(file, name):
                file_data = getattr(file, name)
                data = np.zeros_like(file_data)
                data[:] = file_data
                points[name] = _get_attribute(data, data.dtype.name)

        return {keys.point: points}

    def write(self, point_cloud, attributes='all', file_version='1.2', point_format=3):
        """
        Write point cloud to a LAS(LAZ) file.

        :param point_cloud:
        :param attributes: list of attributes to write ('all' for all attributes in point_cloud)
        :param file_version:
        :param point_format:
        :return:
        """
        file = laspy.create(point_format=point_format,
                            file_version=file_version)

        points = point_cloud[keys.point]
        attributes = select_valid_attributes([attr for attr in points.keys()], attributes)

        # NOTE: adding extra dims and assignment should be done in two steps,
        # some fields (e.g. raw_classification) are otherwise overwritten
        dtype = file.header.point_format.dtype()
        for attribute in attributes:
            data, type = _get_data_and_type(points[attribute])
            type_short = convert_to_short_type(type)
            if attribute not in 'xyz':
                # x,y,z are not there but file methods can be used to convert coords to int4
                if attribute not in dtype.fields:
                    param = laspy.ExtraBytesParams(name=attribute, type=type)
                    file.add_extra_dim(param)
            file_type_short = convert_to_short_type(getattr(file, attribute).dtype.name)
            if not file_type_short == type_short:
                raise TypeError('Data type in file does not match the one in point cloud: '
                                'for {}, {} vs {}'.format(attribute, file_type_short, type_short))

        for dim in 'xyz':
            data, _ = _get_data_and_type(points[dim])
            setattr(file.header, '{}_offset'.format(dim), data.min())
            setattr(file.header, '{}_scale'.format(dim), 0.001)

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
                             'laspy error below:\n{}'.format(file_version, point_format, err))


def _get_attribute(data, data_type):
    return {'type': data_type, 'data': data}


def _get_data_and_type(attribute):
    return attribute['data'], attribute['type']
