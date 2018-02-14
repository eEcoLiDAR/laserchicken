import os
import random
import unittest

from laserchicken import read_las
from laserchicken.feature_extractor.percentile_feature_extractor import PercentileFeatureExtractor


class TestPercentileFeatureExtractor(unittest.TestCase):

    @staticmethod
    def test_percentile():
        """Compute the percentile of a given selection."""
        print(os.getcwd())
        print(os.path.exists("testdata/AHN2.las"))
        pc_in = read_las.read("testdata/AHN2.las")
        indices = [
            89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591, 7018, 61494,
            65194, 117931, 62971, 10474, 90322
        ]
        extractor = PercentileFeatureExtractor()
        per = extractor.extract(pc_in, indices, None, None, None)

        test_values = [
            0.5199999737739562, 0.5639999737739563, 0.5899999737739563, 0.6519999737739564, 0.6999999737739563,
            0.9239999737739564, 1.0169999737739561, 2.417999973773957, 2.9339999737739566, 5.979999973773956
        ]

        for _, val, tar in zip(extractor.provides(), per, test_values):
            assert val == tar

    def setUp(self):
        random.seed(20)

    def tearDowm(self):
        pass


if __name__ == '__main__':
    unittest.main()
