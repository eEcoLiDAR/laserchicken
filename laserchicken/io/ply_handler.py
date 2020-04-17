""" IO handler for PLY file format """
from laserchicken.io.base_io_handler import IOHandler
from laserchicken.io.ply_read import read
from laserchicken.io.ply_write import write


class PLYHandler(IOHandler):
    """ Class for IO of point-cloud data in PLY file format """

    def read(self):
        return read(self.path)

    def write(self, point_cloud, *args, **kwargs):
        write(point_cloud, self.path, *args, **kwargs)
