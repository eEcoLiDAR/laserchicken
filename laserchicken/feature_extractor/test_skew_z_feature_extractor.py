import unittest

import numpy as np

from laserchicken import load, keys
from laserchicken.feature_extractor.skew_feature_extractor import SkewFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestSkewZFeatureExtractorReal(unittest.TestCase):
    def test_height_stats(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        skew_z = self.extractor.extract(pc_in, [neighborhood], None, None, None)[0]
        np.testing.assert_allclose(skew_z, 2.083098281031817)

    def test_height_stats_without_neighbors(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = []
        skew_z = self.extractor.extract(pc_in, [neighborhood], pc_in, None, None)[0]
        assert np.isnan(skew_z)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('skew_z', feature_names)

    def setUp(self):
        self.extractor = SkewFeatureExtractor()


class TestSkewZFeatureExtractor(unittest.TestCase):
    def test_use_norm_z(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 6])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        skew = self.extractor.extract(point_cloud, [neighborhood], None, None, None)[0]

        self.assertGreater(skew, 0.1)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('skew_normalized_height', feature_names)

    def setUp(self):
        self.extractor = SkewFeatureExtractor(data_key=keys.normalized_height)
