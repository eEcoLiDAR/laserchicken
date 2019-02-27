import unittest

import numpy as np

from laserchicken.feature_extractor.range_norm_z_feature_extractor import RangeNormZFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestRangeNormZFeatureExtractor(unittest.TestCase):
    def test_use_norm(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        extractor = RangeNormZFeatureExtractor()
        _max, _min, _range = extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertAlmostEquals(_max, 5)
        self.assertAlmostEquals(_min, 3)
        self.assertAlmostEquals(_range, 2)
