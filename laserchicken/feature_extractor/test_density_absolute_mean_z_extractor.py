import unittest

import numpy as np

from laserchicken.feature_extractor.density_absolute_mean_z_feature_extractor import \
    DensityAbsoluteMeanZFeatureExtractor
from laserchicken.keys import point
from laserchicken.test_tools import create_point_cloud


class TestDensityAbsoluteMeanZFeatureExtractorArtificialData(unittest.TestCase):
    def test_simle_case_correct(self):
        """Check that one out of 4 points above mean of only vegetation points yields a value of 25"""
        ground = 2  # Ground tag
        veg = 4  # Medium vegetation tag
        x = y = z = np.array([10, 10, 10, 1, 1, 1, 2])
        point_cloud = create_point_cloud(x, y, z)
        point_cloud[point]['raw_classification'] = {'data': np.array([ground, ground, ground, veg, veg, veg, veg]),
                                                    'type': 'double'}
        neighborhood = list(range(len(x)))

        extractor = DensityAbsoluteMeanZFeatureExtractor()
        density_absolute_mean = extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertAlmostEqual(density_absolute_mean, 25)


if __name__ == '__main__':
    unittest.main()
