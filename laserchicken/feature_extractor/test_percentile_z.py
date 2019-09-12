import os
import random
import unittest
import itertools
import numpy as np
from laserchicken import read_las, keys
from laserchicken.feature_extractor.percentile_z_feature_extractor import PercentileZFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestPercentileZFeatureExtractorArtificialData(unittest.TestCase):
    """Test percentile feature extractor on artificial data."""

    def test_percentile_z(self):
        xyz = np.array([list(p) for p in list(itertools.product(np.linspace(0, 1, 11), repeat=3))])
        point_cloud = create_point_cloud(xyz[:, 0], xyz[:, 1], xyz[:, 2])
        expected = np.linspace(0.1, 1.0, 10)
        extractors = [PercentileZFeatureExtractor(p) for p in range(10, 110, 10)]

        percentiles = [e.extract(point_cloud, range(len(xyz)), None, None, None) for e in extractors]

        np.testing.assert_allclose(percentiles, expected)


class TestPercentileFeatureExtractorRealData(unittest.TestCase):
    """Test percentile feature extractor on real data."""

    def test_percentile(self):
        """Compute the percentile of a given selection."""
        _test_file_name = 'AHN3.las'
        _test_data_source = 'testdata'

        point_cloud = read_las.read(os.path.join(_test_data_source, _test_file_name))
        index = [
            89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591, 7018, 61494,
            65194, 117931, 62971, 10474, 90322
        ]
        extractor = PercentileZFeatureExtractor()

        extractor.extract(point_cloud, index, None, None, None)


if __name__ == '__main__':
    unittest.main()
