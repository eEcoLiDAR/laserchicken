import os
import random
import unittest

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractEigenValues(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_eigenvalues_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        target_point_cloud = utils.copy_pointcloud(self.point_cloud, rand_indices)
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        radius = 2.5
        result_index_lists = compute_neighbors.compute_cylinder_neighborhood_indices(
            self.point_cloud, target_point_cloud, radius)
        feature_extractor.compute_features(self.point_cloud, result_index_lists, target_point_cloud,
                                           ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))
        for i in range(n_targets):
            lambda1, lambda2, lambda3 = utils.get_features(target_point_cloud, i, ["eigenv_1", "eigenv_2", "eigenv_3"])
            self.assertTrue(lambda1 >= lambda2 >= lambda3)
        self.assertEqual("laserchicken.feature_extractor.eigenvals_feature_extractor",
                         target_point_cloud[keys.provenance][0]["module"])

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass
