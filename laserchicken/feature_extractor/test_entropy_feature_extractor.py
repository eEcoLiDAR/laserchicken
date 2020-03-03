import os
import random
import unittest

import numpy as np

from laserchicken import compute_features, keys, load, utils
from laserchicken.compute_neighbors import compute_cylinder_neighborhood
from laserchicken.feature_extractor.entropy_feature_extractor import EntropyFeatureExtractor
from laserchicken.feature_extractor.feature_extraction import compute_features
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractEntropy(unittest.TestCase):
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_entropy_positive_value(self):
        """Test computing of eigenvalues in cylinder."""
        target_point_cloud = self._find_neighbors_for_random_targets_and_compute_entropy()
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])

        for i in range(n_targets):
            entropy_z = utils.get_attribute_value(target_point_cloud, i, "entropy_z")
            self.assertTrue(entropy_z >= 0)

    def test_entropy_parameters_in_log(self):
        """Test if parameters were written to log."""
        expected_parameters = [0.1, None, None]
        target_point_cloud = self._find_neighbors_for_random_targets_and_compute_entropy()
        self.assertEqual(expected_parameters, target_point_cloud[keys.provenance][-1]["parameters"])

    def test_entropy_module_name_in_log(self):
        """Test if parameters were written to log."""
        target_point_cloud = self._find_neighbors_for_random_targets_and_compute_entropy()
        desired_module_name = 'laserchicken.feature_extractor.entropy_feature_extractor'
        self.assertEqual(desired_module_name, target_point_cloud[keys.provenance][-1]["module"])

    def _find_neighbors_for_random_targets_and_compute_entropy(self):
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for _ in range(20)]
        target_point_cloud = utils.copy_point_cloud(self.point_cloud, rand_indices)
        radius = 25
        neighborhoods = list(compute_cylinder_neighborhood(self.point_cloud, target_point_cloud, radius))
        compute_features(self.point_cloud, neighborhoods, target_point_cloud, ["entropy_z"],
                         InfiniteCylinder(5), layer_thickness=0.1)
        return target_point_cloud

    def test_default_provides_correct(self):
        feature_names = EntropyFeatureExtractor().provides()
        self.assertIn('entropy_z', feature_names)

    def setUp(self):
        self.point_cloud = load(os.path.join(self._test_data_source, self._test_file_name))
        random.seed(102938482634)


class TestExtractNormalizedEntropy(unittest.TestCase):
    def test_use_norm_z(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhoods = [[0, 1, 2]]

        entropy = self.extractor.extract(point_cloud, neighborhoods, None, None, None)[0]

        self.assertNotAlmostEqual(entropy, 0)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('entropy_normalized_height', feature_names)

    def setUp(self):
        self.extractor = EntropyFeatureExtractor(data_key=keys.normalized_height)
