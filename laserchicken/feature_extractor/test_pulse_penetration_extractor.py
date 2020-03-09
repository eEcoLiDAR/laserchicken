import os
import random
import unittest

import numpy as np

from laserchicken import keys, load, utils
from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken.feature_extractor.pulse_penetration_feature_extractor import PulsePenetrationFeatureExtractor
from laserchicken.volume_specification import InfiniteCylinder


class TestPulsePenetrationFeatureExtractorArtificialData(unittest.TestCase):
    """Test the pulse extractor on artificial data."""

    def test_pulse(self):
        """Pulse extractor on artificial data should yield expected feature values."""
        extractor = PulsePenetrationFeatureExtractor()
        pp_ratio = extractor.extract(self.point_cloud, [self.neighborhood], None, None, None)[0]
        self.assertEqual(pp_ratio, self.expected_pp_ratio)

    def _set_plane_data(self):
        """Create two planes of ground point at z = +- 0.1."""
        n_points = 10
        pos = np.linspace(-self.radius, self.radius, n_points)
        self.points_per_plane = 2 * n_points ** 2
        for z in [-0.1, 0.1]:
            for x in pos:
                for y in pos:
                    self.xyz.append([x, y, z])
                    self.pt_type.append(2)

    def _set_sphere_data(self):
        """Create a sphere of vegetation point centered at 0."""
        nteta, nphi = 11, 11
        self.npt_sphere = nteta * nphi
        teta = np.linspace(0.1, 2 * np.pi, nteta)
        phi = np.linspace(0.1, np.pi, nphi)
        r = self.radius
        for t in teta:
            for p in phi:
                x = r * np.cos(t) * np.sin(p)
                y = r * np.sin(t) * np.sin(p)
                z = r * np.cos(p)
                self.xyz.append([x, y, z])
                self.pt_type.append(np.random.randint(3, 6))

    def _get_pc(self):
        return {keys.point: {'x': {'type': 'double', 'data': self.xyz[:, 0]},
                             'y': {'type': 'double', 'data': self.xyz[:, 1]},
                             'z': {'type': 'double', 'data': self.xyz[:, 2]},
                             'raw_classification': {'type': 'int', 'data': self.pt_type}}}, len(self.xyz)

    def setUp(self):
        """Set up the data for the test."""
        # set up the point cloud
        self.radius = 0.5
        self.xyz, self.pt_type = [], []
        self._set_sphere_data()
        self._set_plane_data()
        self.xyz = np.array(self.xyz)
        self.point_cloud, n_points = self._get_pc()

        # get the entire neighborhood
        self.neighborhood = list(range(n_points))

        # theo val
        self.expected_pp_ratio = float(self.points_per_plane) / n_points


class TestPulsePenetratioFeatureExtractorRealData(unittest.TestCase):
    """Test the pulse extractor on real data and make sure it doesn't crash."""
    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None
    target_point_cloud = None
    cyl = None
    target_point_cloud_index = None

    def test_valid(self):
        """Compute the echo ratio for a sphere/cylinder at different target points without crashing."""
        # read the data
        self.point_cloud = load(os.path.join(self._test_data_source, self._test_file_name))

        # get the target point clouds
        random.seed(102938482634)
        self.target_point_cloud = self._get_random_targets()
        self.target_point_cloud_index = 0

        # volume descriptions
        radius = 0.5
        self.cyl = InfiniteCylinder(radius)
        neighborhoods = compute_neighborhoods(self.point_cloud, self.target_point_cloud, self.cyl)

        # extractor
        extractor = PulsePenetrationFeatureExtractor()
        extractor.extract(self.point_cloud, neighborhoods, None, None, None)

    def _get_random_targets(self):
        """Get a random target pc."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points)
                        for _ in range(20)]
        return utils.copy_point_cloud(self.point_cloud, rand_indices)


if __name__ == '__main__':
    unittest.main()
