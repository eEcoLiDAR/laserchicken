import unittest

import numpy as np

from laserchicken import keys
from laserchicken.feature_extractor.feature_extraction import compute_features
from laserchicken.test_tools import create_point_cloud, create_points_in_xy_grid
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractSigmaZ(unittest.TestCase):
    def test_constantValues_result0(self):
        def z_constant(x, y):
            return 2

        assert_std_for_z_function_in_xy_grid(z_constant, 0)

    def test_checkered1sAnd0s_resultHalf(self):
        """Standard deviation of checker pattern of 0s and 1s should be 0.5"""

        def z_checkered(x, y):
            return ((x + y) % 2) + 2

        assert_std_for_z_function_in_xy_grid(z_checkered, 0.5)

    def test_checkered1sAnd0sPlusSkewed_resultHalf(self):
        """Standard deviation of checker pattern of 0s and 1s should be 0.5, adding a plane should not change that"""

        def z_checkered(x, y):
            return ((x + y) % 2) + 2 + x + y

        assert_std_for_z_function_in_xy_grid(z_checkered, 0.5)


def assert_std_for_z_function_in_xy_grid(z_checkered, expected):
    """Assert that the standard deviation of z values in a grid of unit x and y"""
    n_points, points = create_points_in_xy_grid(z_checkered)
    point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
    targets = create_point_cloud([0], [0], [0])
    compute_features(point_cloud, [range(n_points)], targets, [
        'sigma_z'], InfiniteCylinder(10))
    np.testing.assert_almost_equal(
        targets[keys.point]['sigma_z']['data'][0], expected)



