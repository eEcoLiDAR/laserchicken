import os
import shutil
import unittest

import numpy as np

from laserchicken.write_ply import write
from laserchicken.plyfile2las import read_ply


class TestWritePly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'test.ply'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_write_nonExistingFile(self):
        """ Should create a file. """
        pc = self.generateTestPointCloud()
        write(pc, self.test_file_path)
        assert (os.path.exists(self.test_file_path))

    def test_write_sameFileTwice(self):
        """ Should not throw an exception. """
        pc = self.generateTestPointCloud()
        write(pc, self.test_file_path)
        write(pc, self.test_file_path)

    @unittest.skip('Production code for writing not yet implemented.')
    def test_write_loadTheSame(self):
        """ Writing a point cloud and loading it afterwards should result in the same point cloud. """
        pc = self.generateTestPointCloud()
        write(pc, self.test_file_path)
        loaded = read_ply(self.test_file_path)
        np.testing.assert_allclose(loaded, pc)

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)

    @staticmethod
    def generateTestPointCloud():
        pc = {'points': {'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [3, 4, 5]}}
        return pc
