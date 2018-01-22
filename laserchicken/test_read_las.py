"""Test read_las module."""
import os
import shutil
import unittest

import numpy as np
import pytest

from laserchicken import keys
from laserchicken.read_las import read


class TestReadWriteLas(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_load_containsPoints(self):
        """Should run without exception and return points."""
        point_cloud = read(self.test_file_path)
        self.assertIn(keys.point, point_cloud)

    def test_load_PointsContainX(self):
        """Should run without exception and return points."""
        point_cloud = read(self.test_file_path)
        print(point_cloud)
        self.assertIn('data', point_cloud[keys.point]['x'])

    def test_load_CorrectFirstX(self):
        """Should run without exception and compare equal."""
        point_cloud = read(self.test_file_path)
        data = {
            'x': 131999.984125,
            'y': 549718.375,
            'z': -0.34100002,
            'gps_time': 78563787.97322202,
            'intensity': 41,
            'raw_classification': 9,
        }
        names = sorted(data)
        print("Order:", names)
        point = [point_cloud[keys.point][name]['data'][0] for name in names]
        np.testing.assert_allclose(np.array(point), np.array([data[name] for name in names]))

    def test_load_nonexistentFile(self):
        """Should raise exception."""
        with pytest.raises(OSError):
            read('nonexistent.las')

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
