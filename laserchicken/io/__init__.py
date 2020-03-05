import os

from .las_handler import LASHandler as las
from .ply_handler import PLYHandler as ply

io_handlers = {
    '.ply': ply,
    '.las': las,
    '.laz': las,
}


def get_io_handler(path, mode, format=None, overwrite=False):
    """
    Return instance of format-specific IOHandler, already initialized to read or write mode.

    :param path: path where the IO operation needs to take place
    :param mode: 'r' for reading, 'w' for writing
    :param format: point-cloud file format, try to guess it from extension if not specified
    :param overwrite: if working in write mode, allow to overwrite if file exists.
    :return: instance of the IOHandler
    """
    if format is None:
        _root, format = os.path.splitext(path)
    format = format.lower()
    _check_format(format)
    io_handler = io_handlers[format]
    return io_handler(path, mode, overwrite=overwrite)


def _check_format(format):
    if format not in io_handlers:
        raise NotImplementedError(
            "File format %s unknown. Implemented formats are: %s" % (format, ', '.join(io_handlers.keys())))
