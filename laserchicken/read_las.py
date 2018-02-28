"""Module for reading LAS files."""
import os

import laspy

from laserchicken import keys


def read(path):
    """
    Load the points from a LAS file into memory.

    Resulting data structure looks like:
    {'log': ['Processed by module load', 'Processed by module filter using parameters(x,y,z)'],
     'pointcloud':
       {'offset': {'type': 'double', 'data': 12.1}},
     'vertex':
       {'x': {'type': 'double', 'data': np.array([0.1, 0.2, 0.3])},
        'y': {'type': 'double', 'data': np.array([0.1, 0.2, 0.3])},
        'z': {'type': 'double', 'data': np.array([0.1, 0.2, 0.3])},
        'return': {'type': 'int', 'data': np.array([1, 1, 2])}}}
    :param path: is the path to the las file
    :return: point cloud data structure
    """
    if not os.path.exists(path):
        raise OSError('{} not found.'.format(path))

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
