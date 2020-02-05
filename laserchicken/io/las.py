""" IO Handler for LAS (and compressed LAZ) file format """

from laserchicken.io.base_io_handler import IOHandler
from laserchicken.io.read_las import read

class las(IOHandler):
    def read(self):
       return read(self.path)