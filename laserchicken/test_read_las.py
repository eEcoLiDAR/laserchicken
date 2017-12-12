import os
import shutil
import unittest

import numpy as np
import pytest

from laserchicken.read_las import read


class TestReadWriteLas(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = '5points.las'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_load_containsPoints(self):
        """ Should run without exception and return points. """
        point_cloud = read(self.test_file_path)
        self.assertIn('points', point_cloud)

    def test_load_PointsContainX(self):
        """ Should run without exception and return points. """
        point_cloud = read(self.test_file_path)
        print(point_cloud)
        self.assertIn('data', point_cloud['points']['x'])

    def test_load_CorrectFirstX(self):
        """ Should . """
        point_cloud = read(self.test_file_path)
        point = [point_cloud['points']['x']['data'][0],
                 point_cloud['points']['y']['data'][0],
                 point_cloud['points']['z']['data'][0]]
        np.testing.assert_allclose(np.array(point),
                                   np.array([-1870.480059509277, 338897.281499328557, 192.363999260664]))

    def test_load_nonexistentFile(self):
        """ Should raise exception. """
        with pytest.raises(OSError):
            read('nonexistent.las')

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
