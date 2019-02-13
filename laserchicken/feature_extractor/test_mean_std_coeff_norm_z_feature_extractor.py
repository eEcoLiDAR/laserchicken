import unittest

import numpy as np

from laserchicken.feature_extractor.mean_std_coeff_norm_z_feature_extractor import MeanStdCoeffNormZFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestMeanStdCoeffNormZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        extractor = MeanStdCoeffNormZFeatureExtractor()
        mean, std, coeff = extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertAlmostEquals(mean, 4)
        self.assertAlmostEquals(std, np.sqrt(2/3))
        self.assertAlmostEquals(coeff, np.sqrt(2/3)/4)
