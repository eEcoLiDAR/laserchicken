import random
import unittest

import numpy as np
from laserchicken import read_las
from laserchicken.feature_extractor.height_statistics_feature_extractor import HeightStatisticsFeatureExtractor


class TestHeightStatisticsFeatureExtractor(unittest.TestCase):

    def test_height_stats(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591, 7018,
                   61494, 65194, 117931, 62971, 10474, 90322]
        extractor = HeightStatisticsFeatureExtractor()
        (max_z, min_z, mean_z, median_z, std_z, var_z, range_z, coeff_var_z, skew_z, kurto_z) = extractor.extract(
            pc_in, neighborhood, None, None, None)
        print(max_z, min_z, mean_z, median_z, std_z,
              var_z, range_z, coeff_var_z, skew_z, kurto_z)
        assert (max_z == 5.979999973773956)
        assert (min_z == 0.47999997377395631)
        assert (mean_z == 1.3779999737739566)
        assert (median_z == 0.69999997377395629)
        assert (std_z == 1.3567741153191268)
        assert (var_z == 1.8408359999999995)
        assert (range_z == 5.5)
        assert (coeff_var_z == 0.9845966191155302)
        assert (skew_z == 2.083098281031817)
        assert (kurto_z == 3.968414258629714)

    def test_height_stats_without_neighbors(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = []
        extractor = HeightStatisticsFeatureExtractor()
        (max_z, min_z, mean_z, median_z, std_z, var_z, range_z, coeff_var_z, skew_z, kurto_z) = extractor.extract(
            pc_in, neighborhood, pc_in, None, None)
        print(max_z, min_z, mean_z, median_z, std_z,
              var_z, range_z, coeff_var_z, skew_z, kurto_z)
        assert np.isnan(max_z)
        assert np.isnan(min_z)
        assert np.isnan(mean_z )
        assert np.isnan(median_z )
        assert np.isnan(std_z )
        assert np.isnan(var_z )
        assert np.isnan(range_z)
        assert np.isnan(coeff_var_z)
        assert np.isnan(skew_z)
        assert np.isnan(kurto_z)

    def setUp(self):
        random.seed(20)

    def tearDown(self):
        pass
