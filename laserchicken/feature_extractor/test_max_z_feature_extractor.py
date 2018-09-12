import random
import unittest

import numpy as np

from laserchicken import read_las
from laserchicken.feature_extractor.max_z_feature_extractor import MaxZFeatureExtractor


class TestMaxZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        max_z = MaxZFeatureExtractor().extract(
            pc_in, neighborhood, None, None, None)

        np.testing.assert_allclose(max_z, 5.979999973773956)

    def test_height_stats_without_neighbors(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = []
        max_z = MaxZFeatureExtractor().extract(pc_in, neighborhood, pc_in, None, None)
        assert np.isnan(max_z)

    def setUp(self):
        random.seed(20)

    def tearDown(self):
        pass
