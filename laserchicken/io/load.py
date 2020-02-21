import sys
from laserchicken.io import get_io_handler
from laserchicken.utils import add_metadata


def load(path, format=None, *args, **kwargs):
    """
    Read point cloud from a file.

    :param path:
    :param format:
    :param args: optional non-keyword arguments to be passed to the format-specific writer
    :param kwargs: optional keyword arguments to be passed to the format-specific writer
    :return: point cloud data
    """
    reader = get_io_handler(path, mode='r', format=format)
    point_cloud = reader.read(*args, **kwargs)
    add_metadata(point_cloud, sys.modules[__name__], {'path': path, 'args': args, **kwargs})
    return point_cloud
