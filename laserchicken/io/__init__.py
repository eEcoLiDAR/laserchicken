from .las import las
from .ply import ply

io_handlers = {
    'ply': ply,
    'las': las,
    'laz': las,
}

def get_io_handler(path, mode, format=None, overwrite=False):
    if format is None:
        format = path.split('.')[-1]
    format = format.lower()
    check_format(format)
    io_handler = io_handlers[format]
    return io_handler(path, mode, overwrite=overwrite)

def check_format(format):
    if format in io_handlers:
        pass
    else:
        raise NotImplementedError(
            "File format %s not recognized. Implemented formats are: %s" % (format, ', '.join(io_handlers.keys())))