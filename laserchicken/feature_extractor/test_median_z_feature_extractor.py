import unittest

import numpy as np

from laserchicken import load, keys
from laserchicken.feature_extractor.median_feature_extractor import MedianFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestMedianZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        median_z = self.extractor.extract(pc_in, [neighborhood], None, None, None)[0]
        np.testing.assert_allclose(median_z, 0.69999997377395629)

    def test_height_stats_without_neighbors(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = []
        median_z = self.extractor.extract(pc_in, [neighborhood], pc_in, None, None)[0]
        assert np.isnan(median_z)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('median_z', feature_names)

    def setUp(self):
        self.extractor = MedianFeatureExtractor()


class TestMedianNormZFeatureExtractor(unittest.TestCase):
    def test_use_norm_z(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 6])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        median = self.extractor.extract(point_cloud, neighborhood, None, None, None)

        np.testing.assert_almost_equal(median, 4)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('median_normalized_height', feature_names)

    def setUp(self):
        self.extractor = MedianFeatureExtractor(data_key=keys.normalized_height)
