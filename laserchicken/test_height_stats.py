import random
import unittest

from laserchicken.height_stats import heightStatistics
from laserchicken import read_las, keys

class TestHeightStats(unittest.TestCase):

    @staticmethod
    def test_height_stats():
        pc_in = read_las.read("testdata/AHN2.las")
        num_all_pc_points = len(pc_in[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        (max_z, min_z, mean_z, median_z, std_z, var_z, range, coeff_var_z, skew_z, kurto_z) = heightStatistics.extract(pc_in, rand_indices, None, None)
        assert (max_z == 0)
        assert (min_z == 0)
        assert (mean_z == 0)
        assert (median_z == 0)
        assert (std_z == 0)
        assert (var_z == 0)
        assert (range == 0)
        assert (coeff_var_z == 0)
        assert (skew_z == 0)
        assert (kurto_z == 0)