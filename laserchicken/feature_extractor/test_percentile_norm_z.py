import itertools
import unittest

import numpy as np

from laserchicken.feature_extractor.percentile_norm_z_feature_extractor import PercentileNormZFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestPercentileNormZFeatureExtractorArtificialData(unittest.TestCase):
    """Test percentile feature extractor on artificial data."""

    def test_percentile_norm_z(self):
        xyz = np.array([list(p) for p in list(itertools.product(np.linspace(0, 1, 11), repeat=3))])
        point_cloud = create_point_cloud(xyz[:, 0], xyz[:, 1], np.zeros_like(xyz[:, 2]), normalized_z=xyz[:, 2])
        expected = np.linspace(0.1, 1.0, 10)
        extractors = [PercentileNormZFeatureExtractor(p) for p in range(10, 110, 10)]

        percentiles = np.hstack([e.extract(point_cloud, range(len(xyz)), None, None, None) for e in extractors])

        np.testing.assert_allclose(percentiles, expected)

if __name__ == '__main__':
    unittest.main()
