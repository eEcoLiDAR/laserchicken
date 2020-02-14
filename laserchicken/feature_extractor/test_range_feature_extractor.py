import unittest

import numpy as np

from laserchicken import load, keys
from laserchicken.feature_extractor.range_feature_extractor import RangeFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestRangeZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        max_z, min_z, range_z = RangeFeatureExtractor().extract(pc_in, [neighborhood], None, None, None)[:, 0]
        np.testing.assert_allclose(range_z, 5.5)
        np.testing.assert_allclose(max_z, 5.979999973773956)
        np.testing.assert_allclose(min_z, 0.47999997377395631)

    def test_height_stats_without_neighbors(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = []
        max_z, min_z, range_z = RangeFeatureExtractor().extract(pc_in, [neighborhood], pc_in, None, None)[:, 0]
        assert np.isnan(range_z)
        assert np.isnan(max_z)
        assert np.isnan(min_z)

    def test_default_provides_correct(self):
        feature_names = RangeFeatureExtractor().provides()
        self.assertIn('min_z', feature_names)
        self.assertIn('max_z', feature_names)
        self.assertIn('range_z', feature_names)


class TestRangeNormZFeatureExtractor(unittest.TestCase):
    def test_use_norm(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        extractor = RangeFeatureExtractor(data_key=keys.normalized_height)
        _max, _min, _range = extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertAlmostEqual(_max, 5)
        self.assertAlmostEqual(_min, 3)
        self.assertAlmostEqual(_range, 2)

    def test_normalized_z_provides_correct(self):
        feature_names = RangeFeatureExtractor(data_key=keys.normalized_height).provides()
        self.assertIn('min_normalized_height', feature_names)
        self.assertIn('max_normalized_height', feature_names)
        self.assertIn('range_normalized_height', feature_names)
