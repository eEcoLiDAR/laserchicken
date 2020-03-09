import itertools
import os
import unittest

import numpy as np

from laserchicken import load, keys
from laserchicken.feature_extractor.percentile_feature_extractor import PercentileFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestPercentileZFeatureExtractorArtificialData(unittest.TestCase):
    """Test percentile feature extractor on artificial data."""

    def test_percentile_z(self):
        xyz = np.array([list(p) for p in list(itertools.product(np.linspace(0, 1, 11), repeat=3))])
        point_cloud = create_point_cloud(xyz[:, 0], xyz[:, 1], xyz[:, 2])
        expected = np.linspace(0.1, 1.0, 10)
        extractors = [PercentileFeatureExtractor(p) for p in range(10, 110, 10)]

        percentiles = [e.extract(point_cloud, [range(len(xyz))], None, None, None)[0] for e in extractors]

        np.testing.assert_allclose(percentiles, expected)

    def test_default_provides_correct(self):
        feature_names = PercentileFeatureExtractor(54).provides()
        self.assertIn('perc_54_z', feature_names)


class TestPercentileFeatureExtractorRealData(unittest.TestCase):
    """Test percentile feature extractor on real data."""

    def test_percentile(self):
        """Compute the percentile of a given selection."""
        _test_file_name = 'AHN3.las'
        _test_data_source = 'testdata'

        point_cloud = load(os.path.join(_test_data_source, _test_file_name))
        index = [
            89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591, 7018, 61494,
            65194, 117931, 62971, 10474, 90322
        ]
        extractor = PercentileFeatureExtractor()

        extractor.extract(point_cloud, index, None, None, None)


class TestPercentileNormZFeatureExtractorArtificialData(unittest.TestCase):
    """Test percentile feature extractor on artificial data."""

    def test_percentile_norm_z(self):
        xyz = np.array([list(p) for p in list(itertools.product(np.linspace(0, 1, 11), repeat=3))])
        point_cloud = create_point_cloud(xyz[:, 0], xyz[:, 1], np.zeros_like(xyz[:, 2]), normalized_z=xyz[:, 2])
        expected = np.linspace(0.1, 1.0, 10)
        extractors = [PercentileFeatureExtractor(p, data_key=keys.normalized_height) for p in range(10, 110, 10)]

        percentiles = np.hstack([e.extract(point_cloud, [range(len(xyz))], None, None, None)[0] for e in extractors])

        np.testing.assert_allclose(percentiles, expected)

    def test_default_provides_correct(self):
        feature_names = PercentileFeatureExtractor(54, data_key=keys.normalized_height).provides()
        self.assertIn('perc_54_normalized_height', feature_names)
