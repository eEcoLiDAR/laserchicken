import os

import laspy

from laserchicken import keys


def read(path):
    """
    Loads the points from a LAS file into memory.
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
    print(file.header.scale)
    points = {'x': _get_attribute(_compute_value(file.X, file.header.scale[0], file.header.offset[0]), 'double'),
              'y': _get_attribute(_compute_value(file.Y, file.header.scale[1], file.header.offset[1]), 'double'),
              'z': _get_attribute(_compute_value(file.Z, file.header.scale[2], file.header.offset[2]), 'double')}
    return {keys.point: points}


def _compute_value(data, scale, offset):
    return data * scale + offset


def _get_attribute(data, data_type):
    return {'type': data_type, 'data': data}
