import unittest

import numpy as np

from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import Cell


class TestBandRatioFeatureExtractorSimpleArtificialData(unittest.TestCase):
    """Test echo ratio extractor on artificial spherical and cylindric data."""

    def test_simple_case_correct(self):
        n_below_limit = 10
        n_within = 40
        n_above_limit = 50

        x = np.zeros(n_below_limit+n_within+n_above_limit)
        y = x.copy()
        z = x.copy()
        z[0:n_below_limit] = -1
        z[n_below_limit:n_within+n_below_limit] = 4
        z[n_within+n_below_limit:n_below_limit+n_within+n_above_limit] = 11
        point_cloud = create_point_cloud(x, y, z)
        targets = create_point_cloud(np.array([0]), np.array([0]), np.array([0]))
        extractor = BandRatioFeatureExtractor(3, 5)
        expected = n_within/(n_below_limit+n_within+n_above_limit)

        result = extractor.extract(point_cloud, [list(range(100))], targets, 0, Cell(4))

        np.testing.assert_allclose(result, [expected])

    def test_masked_case_correct(self):
        n_below_limit = 10
        n_within = 40
        n_above_limit = 50
        n_nan = 20
        expected = n_within/(n_below_limit+n_within+n_above_limit)

        self.assert_expected_ratio(n_below_limit, n_within, n_above_limit, n_nan, expected)

    def assert_expected_ratio(self, n_below_limit, n_within, n_above_limit, n_nan, expected):
        x = np.zeros(n_below_limit + n_within + n_above_limit + n_nan)
        y = x.copy()
        z = x.copy()
        z[0:n_below_limit] = -1
        z[n_below_limit:n_within + n_below_limit] = 4
        z[n_within + n_below_limit:n_below_limit + n_within + n_above_limit] = 11
        z[n_below_limit + n_within + n_above_limit:] = np.nan
        point_cloud = create_point_cloud(x, y, z)
        targets = create_point_cloud(np.array([0]), np.array([0]), np.array([0]))
        extractor = BandRatioFeatureExtractor(3, 5)
        result = extractor.extract(point_cloud, [list(range(100))], targets, 0, Cell(4))
        np.testing.assert_allclose(result, [expected])
