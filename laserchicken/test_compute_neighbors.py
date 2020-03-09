import os
import random
import unittest

import numpy as np
from numpy.testing import assert_equal

from laserchicken import kd_tree, keys, load, utils
from laserchicken.compute_neighbors import compute_neighborhoods, compute_cylinder_neighborhood, \
    compute_sphere_neighborhood
from laserchicken.test_tools import create_point_cloud, create_points_in_xy_grid
from laserchicken.volume_specification import Sphere, InfiniteCylinder, Cell, Cube


class TestComputeNeighbors(unittest.TestCase):
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_compute_cylinder_neighbors(self):
        """Compute neighbors should only return points within the (xy) radius of the target."""
        target_point_cloud = self._get_random_targets()
        radius = 0.5
        neighborhoods = list(compute_cylinder_neighborhood(self.point_cloud, target_point_cloud, radius))
        self._assert_all_points_within_cylinder(neighborhoods, target_point_cloud, radius)

    def test_compute_sphere_neighbors(self):
        """Compute neighbors should only return points within the (xyz) radius of the target."""
        target_point_cloud = self._get_random_targets()
        radius = 0.5
        neighborhoods = list(compute_sphere_neighborhood(self.point_cloud, target_point_cloud, radius))
        self._assert_all_points_within_sphere(neighborhoods, target_point_cloud, radius)

    def test_compute_neighbors_sphereVolume(self):
        """Compute neighbors should detect sphere volume and find neighbors accordingly"""
        target_point_cloud = self._get_random_targets()
        sphere = Sphere(0.5)
        neighborhoods = compute_neighborhoods(self.point_cloud, target_point_cloud, sphere)
        self._assert_all_points_within_sphere(neighborhoods, target_point_cloud, sphere.radius)

    def test_compute_neighbors_cylinderVolume(self):
        """Compute neighbors should detect cylinder volume and find neighbors accordingly"""
        target_point_cloud = self._get_random_targets()
        cylinder = InfiniteCylinder(0.5)
        neighborhoods = compute_neighborhoods(self.point_cloud, target_point_cloud, cylinder)
        self._assert_all_points_within_cylinder(neighborhoods, target_point_cloud, cylinder.radius)

    def test_cell_no_points(self):
        point_cloud = create_emtpy_point_cloud()
        targets = create_point_cloud(np.zeros(1), np.zeros(1), np.zeros(1))
        neighborhoods = list(compute_neighborhoods(point_cloud, targets, Cell(1)))
        assert_equal(len(neighborhoods[0]), 0)

    def test_cell_grid(self):
        _, points = create_points_in_xy_grid(lambda x, y: np.random.rand())
        point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
        targets = create_point_cloud(np.array([4.5]), np.array([4.5]), np.array([4.5]))  # Center of grid
        neighborhoods = list(compute_neighborhoods(point_cloud, targets, Cell(2)))
        assert_equal(len(neighborhoods[0]), 4)

    def test_cell_grid_sample_size(self):
        _, points = create_points_in_xy_grid(lambda x, y: np.random.rand())
        point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
        targets = create_point_cloud(np.array([4.5]), np.array([4.5]), np.array([4.5]))  # Center of grid
        neighborhoods = list(compute_neighborhoods(point_cloud, targets, Cell(5), sample_size=3))
        assert_equal(len(neighborhoods[0]), 3)

    def test_cell_grid_larger_sample_size(self):
        _, points = create_points_in_xy_grid(lambda x, y: np.random.rand())
        point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
        targets = create_point_cloud(np.array([4.5]), np.array([4.5]), np.array([4.5]))  # Center of grid
        neighborhoods = compute_neighborhoods(point_cloud, targets, Cell(5), sample_size=10000)  # Result 36 neighbors
        _ = next(neighborhoods)

    def test_cell_grid_origin(self):
        _, points = create_points_in_xy_grid(lambda x, y: np.random.rand())
        point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
        targets = create_point_cloud(np.array([0]), np.array([0]), np.array([0]))  # Center of grid
        neighborhoods = list(compute_neighborhoods(point_cloud, targets, Cell(1.99)))
        assert_equal(len(neighborhoods[0]), 1)

    def test_cube_no_points(self):
        point_cloud = create_emtpy_point_cloud()
        targets = create_point_cloud(np.zeros(1), np.zeros(1), np.zeros(1))
        neighborhoods = list(compute_neighborhoods(point_cloud, targets, Cube(1)))
        assert_equal(len(neighborhoods[0]), 0)

    def test_cube_grid(self):
        _, points = create_points_in_xy_grid(lambda x, y: 10 * (x % 2))
        point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
        targets = create_point_cloud(np.array([4.5]), np.array([4.5]), np.array([0]))  # Center of grid
        neighborhoods = list(compute_neighborhoods(point_cloud, targets, Cube(2)))
        assert_equal(len(neighborhoods[0]), 2)

    def test_target_number_matches_neighborhood_number(self):
        _, points = create_points_in_xy_grid(lambda x, y: 10 * (x % 2))
        environment_point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
        assert_target_number_matches_neighborhood_number(environment_point_cloud)

    def test_target_number_matches_neighborhood_number_with_empty_point_cloud(self):
        environment_point_cloud = create_emtpy_point_cloud()
        assert_target_number_matches_neighborhood_number(environment_point_cloud)

    def setUp(self):
        self.point_cloud = load(os.path.join(
            self._test_data_source, self._test_file_name))
        random.seed(102938482634)
        kd_tree.initialize_cache()

    def tearDown(self):
        pass

    def _get_random_targets(self):
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for _ in range(20)]
        return utils.copy_point_cloud(self.point_cloud, rand_indices)

    def _assert_all_points_within_cylinder(self, index_sets, target_point_cloud, radius):
        point_clouds = [utils.copy_point_cloud(self.point_cloud, indices) for indices in index_sets]
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
        point_clouds = [utils.copy_point_cloud(
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


def create_emtpy_point_cloud():
    empty = np.zeros(0)
    point_cloud = create_point_cloud(empty, empty, empty)
    return point_cloud


def assert_target_number_matches_neighborhood_number(environment_point_cloud):
    n_targets = 99
    targets = create_point_cloud(np.array(range(n_targets)), np.array(range(n_targets)), np.array(range(n_targets)))
    neighborhoods = list(compute_neighborhoods(environment_point_cloud, targets, Cube(2)))
    assert_equal(len(neighborhoods), n_targets)
