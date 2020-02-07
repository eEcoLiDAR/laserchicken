"""Module for reading LAS files."""
import laspy

from laserchicken import keys


def read(path):
    """
    Load the points from a LAS file into memory.

    :param path: is the path to the las file
    :return: point cloud data structure
    """
    file = laspy.file.File(path)
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
