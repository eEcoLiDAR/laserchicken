import os
import random
import unittest

import numpy as np
from numpy.testing import assert_equal

from laserchicken import keys, read_las, utils
from laserchicken.compute_neighbors import compute_neighborhoods, compute_cylinder_neighborhood, \
    compute_sphere_neighborhood
from laserchicken.volume_specification import Sphere, InfiniteCylinder


class TestComputeNeighbors(unittest.TestCase):
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_compute_cylinder_neighbors(self):
        """Compute neighbors should only return points within the (xy) radius of the target."""
        target_point_cloud = self._get_random_targets()
        radius = 0.5
        neighbors = compute_cylinder_neighborhood(
            self.point_cloud, target_point_cloud, radius)

        result_index_sets = []
        for x in neighbors:
            result_index_sets += x
        self._assert_all_points_within_cylinder(
            result_index_sets, target_point_cloud, radius)

    def test_compute_sphere_neighbors(self):
        """Compute neighbors should only return points within the (xyz) radius of the target."""
        target_point_cloud = self._get_random_targets()
        radius = 0.5
        neighbors = compute_sphere_neighborhood(
            self.point_cloud, target_point_cloud, radius)
        result_point_clouds = []
        for x in neighbors:
            result_point_clouds += x

        self._assert_all_points_within_sphere(
            result_point_clouds, target_point_cloud, radius)

    def test_compute_neighbors_sphereVolume(self):
        """Compute neighbors should detect sphere volume and find neighbors accordingly"""
        target_point_cloud = self._get_random_targets()
        sphere = Sphere(0.5)
        neighbors = compute_neighborhoods(
            self.point_cloud, target_point_cloud, sphere)
        result_point_clouds = []
        for x in neighbors:
            result_point_clouds += x
        self._assert_all_points_within_sphere(
            result_point_clouds, target_point_cloud, sphere.radius)

    def test_compute_neighbors_cylinderVolume(self):
        """Compute neighbors should detect cylinder volume and find neighbors accordingly"""
        target_point_cloud = self._get_random_targets()
        cylinder = InfiniteCylinder(0.5)
        neighbors = compute_neighborhoods(
            self.point_cloud, target_point_cloud, cylinder)
        result_point_clouds = []
        for x in neighbors:
            result_point_clouds += x
        self._assert_all_points_within_cylinder(
            result_point_clouds, target_point_cloud, cylinder.radius)

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(
            self._test_data_source, self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass

    def _get_random_targets(self):
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points)
                        for p in range(20)]
        return utils.copy_pointcloud(self.point_cloud, rand_indices)

    def _assert_all_points_within_cylinder(self, index_sets, target_point_cloud, radius):
        point_clouds = [utils.copy_pointcloud(
            self.point_cloud, indices) for indices in index_sets]
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        assert_equal(n_targets, len(point_clouds))
        for i in range(n_targets):
            target_x = target_point_cloud[keys.point]["x"]["data"][i]
            target_y = target_point_cloud[keys.point]["y"]["data"][i]
            for j in range(len(point_clouds[i][keys.point]["x"]["data"])):
                neighbor_x = point_clouds[i][keys.point]["x"]["data"][j]
                neighbor_y = point_clouds[i][keys.point]["y"]["data"][j]
                dist = np.sqrt((neighbor_x - target_x) ** 2 +
                               (neighbor_y - target_y) ** 2)
                self.assertTrue(dist <= radius)

    def _assert_all_points_within_sphere(self, index_sets, target_point_cloud, radius):
        point_clouds = [utils.copy_pointcloud(
            self.point_cloud, indices) for indices in index_sets]
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        assert_equal(n_targets, len(point_clouds))
        for i in range(n_targets):
            target_x, target_y, target_z = utils.get_point(
                target_point_cloud, i)
            for j in range(len(point_clouds[i][keys.point]["x"]["data"])):
                neighbor_x, neighbor_y, neighbor_z = utils.get_point(
                    point_clouds[i], j)
                dist = np.sqrt(
                    (neighbor_x - target_x) ** 2 + (neighbor_y - target_y) ** 2 + (neighbor_z - target_z) ** 2)
                self.assertTrue(dist <= radius)
