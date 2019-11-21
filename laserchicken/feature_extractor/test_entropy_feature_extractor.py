import os
import random
import unittest

import numpy as np

from laserchicken import feature_extractor, keys, read_las, utils
from laserchicken.compute_neighbors import compute_cylinder_neighborhood
from laserchicken.feature_extractor.entropy_feature_extractor import EntropyFeatureExtractor
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractEntropy(unittest.TestCase):
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_entropy_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for _ in range(20)]
        target_point_cloud = utils.copy_point_cloud(self.point_cloud, rand_indices)
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        radius = 25
        neighborhoods = list(compute_cylinder_neighborhood(self.point_cloud, target_point_cloud, radius))

        feature_extractor.compute_features(self.point_cloud, neighborhoods, target_point_cloud, ["entropy_z"],
                                           InfiniteCylinder(5), layer_thickness=0.1)


        for i in range(n_targets):
            H = utils.get_attribute_value(target_point_cloud, i, "entropy_z")
            self.assertTrue(H >= 0)
        self.assertEqual("laserchicken.feature_extractor.entropy_feature_extractor",
                         target_point_cloud[keys.provenance][0]["module"])
        self.assertEqual(
            [0.1], target_point_cloud[keys.provenance][0]["parameters"])

    def test_default_provides_correct(self):
        feature_names = EntropyFeatureExtractor().provides()
        self.assertIn('entropy_z', feature_names)

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(
            self._test_data_source, self._test_file_name))
        random.seed(102938482634)


class TestExtractNormalizedEntropy(unittest.TestCase):
    def test_use_norm_z(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        entropy = self.extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertNotAlmostEqual(entropy, 0)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('entropy_normalized_height', feature_names)

    def setUp(self):
        self.extractor = EntropyFeatureExtractor(data_key=keys.normalized_height)