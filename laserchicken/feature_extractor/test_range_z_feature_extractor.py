import unittest

import numpy as np

from laserchicken import read_las
from laserchicken.feature_extractor.range_z_feature_extractor import RangeZFeatureExtractor


class TestRangeZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        max_z, min_z, range_z = RangeZFeatureExtractor().extract(pc_in, neighborhood, None, None, None)
        np.testing.assert_allclose(range_z, 5.5)
        np.testing.assert_allclose(max_z, 5.979999973773956)
        np.testing.assert_allclose(min_z, 0.47999997377395631)

    def test_height_stats_without_neighbors(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = []
        max_z, min_z, range_z = RangeZFeatureExtractor().extract(pc_in, neighborhood, pc_in, None, None)
        assert np.isnan(range_z)
        assert np.isnan(max_z)
        assert np.isnan(min_z)
