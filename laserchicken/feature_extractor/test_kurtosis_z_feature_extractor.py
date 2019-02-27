import unittest

import numpy as np

from laserchicken import read_las
from laserchicken.feature_extractor.kurtosis_z_feature_extractor import KurtosisZFeatureExtractor


class TestKurtosisZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        kurtosis_z = KurtosisZFeatureExtractor().extract(pc_in, neighborhood, None, None, None)
        np.testing.assert_allclose(kurtosis_z, 3.968414258629714)

    def test_height_stats_without_neighbors(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = []
        kurtosis_z = KurtosisZFeatureExtractor().extract(pc_in, neighborhood, pc_in, None, None)
        assert np.isnan(kurtosis_z)
