from laserchicken.io import get_io_handler

def export(point_cloud, path, format=None, overwrite=False, *args, **kwargs):
    """
    Write point cloud data to a file.

    :param point_cloud:
    :param path:
    :param format: point cloud file format
    :param overwrite: if path exists, overwrite
    :param args: optional non-keyword arguments to be passed to the format-specific writer
    :param kwargs: optional keyword arguments to be passed to the format-specific writer
    """
    writer = get_io_handler(path, mode='w', format=format, overwrite=overwrite)
    writer.write(point_cloud, *args, **kwargs)