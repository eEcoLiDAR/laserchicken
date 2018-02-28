import os
import random
import unittest
import itertools
import numpy as np
from laserchicken import read_las, keys
from laserchicken.feature_extractor.percentile_feature_extractor import PercentileFeatureExtractor


class TestPercentileFeatureExtractorArtificialData(unittest.TestCase):
    """Test percentile feature extractor on artificial data."""

    point_cloud = None

    def test_percentile(self):
        extractor = PercentileFeatureExtractor()
        per = extractor.extract(self.point_cloud, self.index, None, None, None)
        test_values = np.linspace(0.1,1.0,10)
        self.assertTrue(np.allclose(per,test_values))

    def _get_data(self):
        """Create a 3D grid of equally spaced points."""

        x = np.linspace(0, 1, 11)
        self.xyz = np.array([ list(p) for p in list(itertools.product(x,repeat=3))])
        self.point_cloud = {keys.point: {'x': {'type': 'double', 'data': self.xyz[:, 0]},
                           'y': {'type': 'double', 'data': self.xyz[:, 1]},
                           'z': {'type': 'double', 'data': self.xyz[:, 2]}}}


    def setUp(self):
        """Set up the test."""
        self._get_data()
        self.index = range(len(self.xyz))

    def tearDowm(self):
        """Tear it down."""
        pass



class TestPercentileFeatureExtractorRealData(unittest.TestCase):
    """Test percentile feature extractor on real data."""

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_percentile(self):
        """Compute the percentile of a given selection."""

        extractor = PercentileFeatureExtractor()
        extractor.extract(self.point_cloud , self.index, None, None, None)

    def setUp(self):
        """Set up the test."""
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))
        self.index = [
            89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591, 7018, 61494,
            65194, 117931, 62971, 10474, 90322
        ]

    def tearDowm(self):
        """Tear it down."""
        pass


if __name__ == '__main__':
    unittest.main()
