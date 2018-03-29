import os
import random
import unittest

import numpy as np

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractEigenValues(unittest.TestCase):
    def test_eigenvalues_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        test_file_name = 'AHN3.las'
        test_data_source = 'testdata'
        random.seed(102938482634)
        point_cloud = read_las.read(
            os.path.join(test_data_source, test_file_name))
        num_all_pc_points = len(point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points)
                        for _ in range(20)]
        target_point_cloud = utils.copy_pointcloud(point_cloud, rand_indices)
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        radius = 2.5
        neighbors = compute_neighbors.compute_cylinder_neighborhood(
            point_cloud, target_point_cloud, radius)

        result_index_lists = []
        for x in neighbors:
            result_index_lists += x

        feature_extractor.compute_features(point_cloud, result_index_lists, target_point_cloud,
                                           ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))

        for i in range(n_targets):
            lambda1, lambda2, lambda3 = utils.get_features(
                target_point_cloud, i, ["eigenv_1", "eigenv_2", "eigenv_3"])
            self.assertTrue(lambda1 >= lambda2 >= lambda3)
        self.assertEqual("laserchicken.feature_extractor.eigenvals_feature_extractor",
                         target_point_cloud[keys.provenance][0]["module"])

    @staticmethod
    def test_eigenvalues_of_too_few_points_results_in_0():
        """If there are too few points to calculate the eigen values we output 0 (as opposed to NaN for example)."""
        a = np.array([5])
        pc = create_point_cloud(a, a, a)

        feature_extractor.compute_features(
            pc, [[0]], pc, ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))

        eigen_val_123 = np.array(
            [pc[keys.point]['eigenv_{}'.format(i)]['data'] for i in [1, 2, 3]])
        np.testing.assert_allclose(eigen_val_123, np.zeros((3, 1)))
