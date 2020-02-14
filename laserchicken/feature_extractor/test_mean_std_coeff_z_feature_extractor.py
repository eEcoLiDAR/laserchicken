import unittest

import numpy as np

from laserchicken import load, keys
from laserchicken.feature_extractor.mean_std_coeff_feature_extractor import MeanStdCoeffFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestMeanZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        mean_z, std_z, coeff_var_z = self.extractor.extract(pc_in, [neighborhood], None, None, None)[:, 0]
        np.testing.assert_allclose(mean_z, 1.3779999737739566)
        np.testing.assert_allclose(std_z, 1.3567741153191268)
        np.testing.assert_allclose(coeff_var_z, 0.9845966191155302)

    def test_height_stats_without_neighbors(self):
        pc_in = load("testdata/AHN2.las")
        neighborhood = []
        mean_z, std_z, coeff_var_z = self.extractor.extract(pc_in, [neighborhood], pc_in, None, None)[:, 0]
        assert np.isnan(mean_z)
        assert np.isnan(std_z)
        assert np.isnan(coeff_var_z)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('mean_z', feature_names)
        self.assertIn('std_z', feature_names)
        self.assertIn('coeff_var_z', feature_names)

    def setUp(self):
        self.extractor = MeanStdCoeffFeatureExtractor()


class TestMeanStdCoeffNormZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        mean, std, coeff = self.extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertAlmostEqual(mean, 4)
        self.assertAlmostEqual(std, np.sqrt(2 / 3))
        self.assertAlmostEqual(coeff, np.sqrt(2 / 3) / 4)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('mean_normalized_height', feature_names)
        self.assertIn('std_normalized_height', feature_names)
        self.assertIn('coeff_var_normalized_height', feature_names)

    def setUp(self):
        self.extractor = MeanStdCoeffFeatureExtractor(data_key=keys.normalized_height)
