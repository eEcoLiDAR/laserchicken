import unittest

import numpy as np
import pytest

from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import Cell, Sphere, Cube, InfiniteCylinder

UPPER_LIMIT = 5
LOWER_LIMIT = 3

VALUE_BELOW_LIMIT = -1
VALUE_WITHIN_LIMITS = 4
VALUE_ABOVE_LIMITS = 11


class TestBandRatioFeatureExtractorSimpleArtificialData(unittest.TestCase):
    """Test echo ratio extractor on artificial spherical and cylindric data."""

    def test_simple_case_correct(self):
        """Ratio of points within with respect to total should be returned."""
        n_below_limit = 10
        n_within = 40
        n_above_limit = 50
        expected_ratio = 0.4  # which is n_within/(n_below_limit+n_within+n_above_limit)

        assert_expected_ratio(expected_ratio, n_below_limit, n_within, n_above_limit)

    def test_mixed_neighborhoods(self):
        expected_ratios = [0.2, 0.6]
        n_below_limits = [20, 0]
        n_withins = [10, 60]
        n_above_limits = [20, 40]
        assert_expected_ratios(expected_ratios, n_below_limits, n_withins, n_above_limits)

    def test_sphere_volume_raise(self):
        with pytest.raises(ValueError):
            assert_expected_ratio(volume=Sphere(5))

    def test_cube_volume_raise(self):
        with pytest.raises(ValueError):
            assert_expected_ratio(volume=Cube(5))

    def test_cell_volume(self):
        assert_expected_ratio(volume=Cell(5))

    def test_cell_volume(self):
        assert_expected_ratio(volume=InfiniteCylinder(5))

    def test_provides(self):
        self.assertEqual(['band_ratio_6-20'], BandRatioFeatureExtractor(6, 20).provides())


def assert_expected_ratio(expected_ratio=0.4, n_below_limit=10, n_within=40, n_above_limit=50, volume=Cell(4)):
    assert_expected_ratios(np.array([expected_ratio]),
                           np.array([n_below_limit]),
                           np.array([n_within]),
                           np.array([n_above_limit]),
                           volume)


def assert_expected_ratios(expected_ratios, n_below_limits, n_withins, n_above_limits, volume=Cell(4)):
    n_ratios = len(expected_ratios)
    neighborhoods, point_cloud = generate_test_point_cloud_and_neighbothoods(n_below_limits,
                                                                             n_withins,
                                                                             n_above_limits,
                                                                             n_ratios)
    targets = create_point_cloud(np.zeros(n_ratios), np.zeros(n_ratios), np.zeros(n_ratios))
    extractor = BandRatioFeatureExtractor(LOWER_LIMIT, UPPER_LIMIT)
    result = extractor.extract(point_cloud, neighborhoods, targets, 0, volume)
    np.testing.assert_allclose(result, expected_ratios)


def generate_test_point_cloud_and_neighbothoods(n_below_limits, n_withins, n_above_limits, n_ratios):
    neighborhoods = []
    cursor = 0
    xs = []
    ys = []
    zs = []
    for i in range(n_ratios):
        x_i, y_i, z_i = generate_test_points(n_below_limits[i], n_withins[i], n_above_limits[i])
        xs.append(x_i)
        ys.append(y_i)
        zs.append(z_i)

        n_neighbors = len(x_i)
        neighborhood = list(range(cursor, cursor + n_neighbors))
        neighborhoods += [neighborhood]
        cursor += n_neighbors

    x = np.hstack(xs)
    y = np.hstack(ys)
    z = np.hstack(zs)
    point_cloud = create_point_cloud(x, y, z)
    return neighborhoods, point_cloud


def generate_test_points(n_below_limit, n_within, n_above_limit):
    """Generate a bunch of daata points on the z axis with the specified number"""
    n_neighbors = n_below_limit + n_within + n_above_limit
    x = np.zeros(n_neighbors)
    y = x.copy()
    z = x.copy()
    z[0:n_below_limit] = VALUE_BELOW_LIMIT
    z[n_below_limit:n_within + n_below_limit] = VALUE_WITHIN_LIMITS
    z[n_within + n_below_limit:n_below_limit + n_within + n_above_limit] = VALUE_ABOVE_LIMITS
    return x, y, z
