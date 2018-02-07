import os
import random
import unittest

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractEntropy(unittest.TestCase):
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_entropy_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        target_point_cloud = utils.copy_pointcloud(self.point_cloud, rand_indices)
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        radius = 25
        result_index_lists = compute_neighbors.compute_cylinder_neighborhood(
            self.point_cloud, target_point_cloud, radius)
        feature_extractor.compute_features(self.point_cloud, result_index_lists, target_point_cloud,
                                           ["z_entropy"], InfiniteCylinder(5), layer_thickness=0.1)
        for i in range(n_targets):
            H = utils.get_feature(target_point_cloud, i, "z_entropy")
            self.assertTrue(H >= 0)
        self.assertEqual("laserchicken.feature_extractor.entropy_feature_extractor",
                         target_point_cloud[keys.provenance][0]["module"])
        self.assertEqual([0.1], target_point_cloud[keys.provenance][0]["parameters"])

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass
