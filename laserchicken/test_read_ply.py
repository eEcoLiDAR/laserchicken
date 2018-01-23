import os
import shutil
import unittest

import numpy as np
from pytest import raises

from laserchicken import keys
from laserchicken.read_ply import read


class TestReadPly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'example.ply'
    _las_file_name = '5points.las'
    _test_data_source = 'testdata'
    las_file_path = os.path.join(_test_dir, _las_file_name)
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_nonexistentFile_error(self):
        # Catch most specific subclass of FileNotFoundException (3.6) and IOError (2.7).
        with raises(Exception):
            read('nonexistentfile.ply')

    def test_wrongFormat_error(self):
        with raises(ValueError):
            read(self.las_file_path)

    def test_existentPly_noError(self):
        read(self.test_file_path)

    def test_containsPointsElement(self):
        data = read(self.test_file_path)
        self.assertIn(keys.point, data)

    def test_containsXElement(self):
        data = read(self.test_file_path)
        self.assertIn('x', data[keys.point])

    def test_rightNumberOfPoints(self):
        data = read(self.test_file_path)
        self.assertEqual(len(data[keys.point]['x']['data']), 3)

    def test_correctPoints(self):
        data = read(self.test_file_path)
        points = data[keys.point]
        point = np.array(
            [points['x']['data'][0], points['y']['data'][0], points['z']['data'][0], points['return']['data'][0]])
        np.testing.assert_allclose(point, np.array([0.11, 0.12, 0.13, 1]))

    def test_correctPointCloud(self):
        data = read(self.test_file_path)
        point_cloud = data['pointcloud']
        offset = point_cloud['offset']['data'][0]
        np.testing.assert_allclose(offset, 12.1)

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)
        shutil.copyfile(os.path.join(self._test_data_source, self._las_file_name), self.las_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
