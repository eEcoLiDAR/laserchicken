import os
import shutil
import unittest

import numpy as np

from laserchicken.read_las import read
from laserchicken.test_utils import generate_test_point_cloud
from laserchicken.write_las import write


class TestReadWriteLas(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = '5points.las'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_writeLas_nonExistentFile_resultExists(self):
        """ Should write a new file. """
        pc = generate_test_point_cloud()
        path = os.path.join(self._test_dir, 'non_existent.las')
        self.assertFalse(os.path.exists(path))
        write(pc, path)
        self.assertTrue(os.path.exists(path))

    @unittest.skip('Production code for writing not yet implemented.')
    def test_writeLas_readLas_same(self):
        """ Reading the file we just wrote should result in same pc. """
        pc = generate_test_point_cloud()
        path = os.path.join(self._test_dir, 'non_existent.las')
        write(pc, path)
        result = read(path)
        for att in ['x', 'y', 'z']:
            np.testing.assert_allclose(result['points'][att]['data'], pc['points'][att]['data'])

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
