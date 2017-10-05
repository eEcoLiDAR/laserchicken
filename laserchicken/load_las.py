import os
import laspy


def load(path):
    if not os.path.exists(path):
        raise OSError('{} not found.'.format(path))

    file = laspy.file.File(path)
    points = {'x': file.get_x, 'y': file.get_y, 'z': file.get_z}
    return {'points': points}
