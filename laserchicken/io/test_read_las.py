"""Test read_las module."""
import os
import shutil
import unittest

import numpy as np
import pytest

from laserchicken import keys
from laserchicken.io.las_handler import DEFAULT_LAS_ATTRIBUTES
from laserchicken.io.load import load


class TestReadLas(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_load_containsPoints(self):
        """Should run without exception and return points."""
        point_cloud = load(self.test_file_path)
        self.assertIn(keys.point, point_cloud)

    def test_load_PointsContainX(self):
        """Should run without exception and return points."""
        point_cloud = load(self.test_file_path)
        print(point_cloud)
        self.assertIn('data', point_cloud[keys.point]['x'])

    def test_load_CorrectFirstX(self):
        """Should run without exception and compare equal."""
        point_cloud = load(self.test_file_path)
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
            load('nonexistent.las')

    def test_load_defaultAttributes(self):
        point_cloud = load(self.test_file_path)
        expected_attributes = [attr for attr in DEFAULT_LAS_ATTRIBUTES]
        _check_expected_attributes(point_cloud, expected_attributes)

    def test_load_allAttributes(self):
        expected_attributes = ['x', 'y', 'z', 'intensity', 'raw_classification',
                               'scan_angle_rank', 'user_data', 'gps_time',
                               'red', 'green', 'blue']
        for attrs in ('all', ['all']):
            point_cloud = load(self.test_file_path, attributes=attrs)
            for attribute in expected_attributes:
                self.assertIn(attribute, point_cloud[keys.point])

    def test_load_specificAttribute(self):
        """Should return only x,y,z"""
        point_cloud = load(self.test_file_path, attributes=['intensity'])
        expected_attributes = ['x', 'y', 'z', 'intensity']
        _check_expected_attributes(point_cloud, expected_attributes)

    def test_load_noAttributes(self):
        """Should return only x,y,z"""
        point_cloud = load(self.test_file_path, attributes=[])
        expected_attributes = ['x', 'y', 'z']
        _check_expected_attributes(point_cloud, expected_attributes)

    def test_load_invalidAttributes(self):
        """Should raise exception."""
        with pytest.raises(ValueError):
            load(self.test_file_path, attributes=None)
        with pytest.raises(ValueError):
            load(self.test_file_path, attributes=['ytisnetni'])

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)


class TestReadLaz(TestReadLas):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'AHN3.laz'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)


def _check_expected_attributes(point_cloud, attributes):
    for attr in attributes:
        assert attr in point_cloud[keys.point].keys()
    assert [attr for attr in point_cloud[keys.point].keys() if attr not in attributes] == []