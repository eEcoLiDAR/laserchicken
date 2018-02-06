import os
import random
import unittest

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils

class TestExtractEntropy(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    pointcloud = None

    def test_entropy_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        num_all_pc_points = len(self.pointcloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        target_pointcloud = utils.copy_pointcloud(self.pointcloud, rand_indices)
        numtargets = len(target_pointcloud[keys.point]["x"]["data"])
        radius = 25
        result_index_lists = compute_neighbors.compute_cylinder_neighborhood_indices(
            self.pointcloud, target_pointcloud, radius)
        feature_extractor.compute_features(self.pointcloud, result_index_lists, target_pointcloud,
                                           ["z_entropy"],layer_thickness = 0.1)
        for i in range(numtargets):
            H = utils.get_feature(target_pointcloud, i, "z_entropy")
            self.assertTrue(H >= 0)
        self.assertEqual("laserchicken.feature_extractor.entropy_feature_extractor",
                         target_pointcloud[keys.provenance][0]["module"])
        self.assertEqual([0.1],target_pointcloud[keys.provenance][0]["parameters"])

    def setUp(self):
        self.pointcloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass
