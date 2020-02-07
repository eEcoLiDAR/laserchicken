""" IO handler for PLY file format """

from laserchicken.io.base_io_handler import IOHandler
from laserchicken.io.read_ply import read
from laserchicken.io.write_ply import write

class PLYHandler(IOHandler):
    def read(self):
        return read(self.path)

    def write(self, point_cloud, *args, **kwargs):
        write(point_cloud, self.path, *args, **kwargs)
