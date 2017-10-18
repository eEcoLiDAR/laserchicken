import os
import laspy


def load(path):
    if not os.path.exists(path):
        raise OSError('{} not found.'.format(path))

    file = laspy.file.File(path)
    points = {'x': file.X, 'y': file.Y, 'z': file.Z}
    return {'points': points}
