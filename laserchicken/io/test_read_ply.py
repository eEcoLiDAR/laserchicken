import os
import shutil
import unittest

import numpy as np
from pytest import raises

from laserchicken import keys
from laserchicken.io.load import load


class TestReadPly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'example.ply'
    _test_file_without_comments_name = 'example_without_comments.ply'
    _test_file_with_invalid_comments_name = 'example_with_invalid_comments.ply'
    _las_file_name = '5points.las'
    _test_data_source = 'testdata'
    las_file_path = os.path.join(_test_dir, _las_file_name)
    test_file_path = os.path.join(_test_dir, _test_file_name)
    test_file_without_comments_path = os.path.join(_test_dir, _test_file_without_comments_name)
    test_file_with_invalid_comments_path = os.path.join(_test_dir, _test_file_with_invalid_comments_name)

    def test_nonexistentFile_error(self):
        # Catch most specific subclass of FileNotFoundException (3.6) and IOError (2.7).
        with raises(Exception):
            load('nonexistentfile.ply')

    def test_wrongFormat_error(self):
        with raises(ValueError):
            load(self.las_file_path, format='.PLY')

    def test_existentPly_noError(self):
        load(self.test_file_path)

    def test_containsPointsElement(self):
        data = load(self.test_file_path)
        self.assertIn(keys.point, data)

    def test_containsXElement(self):
        data = load(self.test_file_path)
        self.assertIn('x', data[keys.point])

    def test_rightNumberOfPoints(self):
        data = load(self.test_file_path)
        self.assertEqual(len(data[keys.point]['x']['data']), 3)

    def test_correctPoints(self):
        data = load(self.test_file_path)
        points = data[keys.point]
        point = np.array(
            [points['x']['data'][0], points['y']['data'][0], points['z']['data'][0], points['return']['data'][0]])
        np.testing.assert_allclose(point, np.array([0.11, 0.12, 0.13, 1]))

    def test_correctPointCloud(self):
        data = load(self.test_file_path)
        point_cloud = data['pointcloud']
        offset = point_cloud['offset']['data'][0]
        np.testing.assert_allclose(offset, 12.1)

    def test_correctPointCloudWithoutComments(self):
        """Missing comment section should not cause error (regression test)."""
        data = load(self.test_file_without_comments_path)
        point_cloud = data['pointcloud']
        offset = point_cloud['offset']['data'][0]
        np.testing.assert_allclose(offset, 12.1)

    def test_correctPointCloudWithInvalidComments(self):
        """Invalid comments should not cause error."""
        data = load(self.test_file_with_invalid_comments_path)
        point_cloud = data['pointcloud']
        offset = point_cloud['offset']['data'][0]
        np.testing.assert_allclose(offset, 12.1)

    def test_allLogEntriesContainAllColumns(self):
        log = load(self.test_file_path)['log']

        for entry in log:
            for key in ['time', 'module', 'parameters', 'version']:
                self.assertIn(key, entry)

    def test_correctModulesLogged(self):
        log = load(self.test_file_path)['log']

        modules = [entry['module'] for entry in log]
        # an additional 'load' is added in the log when reading
        self.assertListEqual(['load', 'filter', 'laserchicken.io.load'], modules)

    def test_correctTimesLogged(self):
        log = load(self.test_file_path)['log']

        self.assertListEqual([2018, 1, 18, 16, 1, 0, 3, 18, -1], list(log[0]['time'].timetuple()))
        self.assertListEqual([2018, 1, 18, 16, 3, 0, 3, 18, -1], list(log[1]['time'].timetuple()))

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_without_comments_name),
                        self.test_file_without_comments_path)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_with_invalid_comments_name),
                        self.test_file_with_invalid_comments_path)
        shutil.copyfile(os.path.join(self._test_data_source, self._las_file_name), self.las_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)


class TestReadPlyBinary(TestReadPly):
    _test_file_name = 'example_little_endian.ply'
    _test_file_without_comments_name = 'example_without_comments_little_endian.ply'
    _test_file_with_invalid_comments_name = 'example_with_invalid_comments_little_endian.ply'
