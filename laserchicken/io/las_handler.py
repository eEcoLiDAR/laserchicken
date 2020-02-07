""" IO Handler for LAS (and compressed LAZ) file format """
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


def _get_attribute(data, data_type):
    return {'type': data_type, 'data': data}
