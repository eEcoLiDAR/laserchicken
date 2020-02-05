from laserchicken.io import get_io_handler

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
    return reader.read(*args, **kwargs)
