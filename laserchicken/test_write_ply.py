import os
import shutil
import unittest

import numpy as np

from laserchicken.write_ply import write
from laserchicken.read_ply import read

from laserchicken.test_utils import generate_simple_test_point_cloud, generate_simple_test_header, generate_complex_test_point_cloud, generate_complex_test_header

def read_header(ply):
    header = ''
    line = ply.readline()
    while line.strip() != 'end_header':
        header = header + line
        line = ply.readline()
    return header

class TestWritePly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'test.ply'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    #@unittest.skip('Production code for writing not yet implemented.')
    def test_write_nonExistingFile(self):
        """ Should create a file. """
        pc = generate_simple_test_point_cloud()
        write(pc, self.test_file_path)
        assert (os.path.exists(self.test_file_path))

    def test_write_sameFileTwice(self):
        """ Should not throw an exception. """
        pc = generate_simple_test_point_cloud()
        write(pc, self.test_file_path)
        write(pc, self.test_file_path)

    def test_write_loadTheSameSimpleHeader(self):
        """  Writing a simple point cloud and loading it afterwards should result in the same point cloud."""
        pc_in = generate_simple_test_point_cloud()
        header_in = generate_simple_test_header()
        write(pc_in, self.test_file_path)
        with open(self.test_file_path,'r') as ply:
            header_out = read_header(ply)
        self.assertMultiLineEqual(header_in, header_out)

    def test_write_loadTheSameComplexHeader(self):
        """  Writing a complex point cloud and loading it afterwards should result in the same point cloud."""
        pc_in = generate_complex_test_point_cloud()
        header_in = generate_complex_test_header()
        write(pc_in, self.test_file_path)
        with open(self.test_file_path,'r') as ply:
            header_out = read_header(ply)
        self.assertMultiLineEqual(header_in, header_out)


    @unittest.skip('Production code for writing not yet implemented.')
    def test_write_loadTheSameData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pass
        """ to finish comparing writing and reading of the same PC
        pc_in = generate_test_point_cloud()
        points_in = data[keys.point]
        write(pc_in, self.test_file_path)
        pc_out = read(self.test_file_path)
        self.asserEqual()
        """

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
