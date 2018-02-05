import os
import random
import unittest

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils


class TestExtractEigenValues(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_eigenvalues_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        target_pointcloud = utils.copy_pointcloud(self.point_cloud, rand_indices)
        numtargets = len(target_pointcloud[keys.point]["x"]["data"])
        radius = 2.5
        result_index_lists = compute_neighbors.compute_cylinder_neighbourhood_indicies(
            self.point_cloud, target_pointcloud, radius)
        feature_extractor.compute_features(self.point_cloud, result_index_lists, target_pointcloud,
                                           ["eigenv_1", "eigenv_2", "eigenv_3"])
        for i in range(numtargets):
            lambda1, lambda2, lambda3 = utils.get_features(target_pointcloud, i, ["eigenv_1", "eigenv_2", "eigenv_3"])
            self.assertTrue(lambda1 >= lambda2 >= lambda3)
        self.assertEqual("laserchicken.feature_extractor.eigenvals_feature_extractor",
                         target_pointcloud[keys.provenance][0]["module"])

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass
