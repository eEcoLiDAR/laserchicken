import os
import random
import unittest
import numpy as np
from laserchicken import keys, read_las, utils
from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken.volume_specification import InfiniteCylinder
from laserchicken.feature_extractor.pulse_penetration_feature_extractor import PulsePenetrationFeatureExtractor


class TestPulsePenetratioFeatureExtractorArtifificalData(unittest.TestCase):
    """Test the pulse extractor on artificial data."""

    def test_pulse(self):

        extractor = PulsePenetrationFeatureExtractor()
        ppratio, densmean = extractor.extract(self.point_cloud, self.neighbhorhood, None, None, None)
        self.assertEqual(ppratio, self.theoval)
        self.assertEqual(densmean, 50.)

    def _set_plane_data(self):
        """Create two planes of ground point at z = +- 0.1."""

        npts = 10
        pos = np.linspace(-self.radius, self.radius, npts)
        self.npt_plane = 2 * npts ** 2
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
        """Set up the data fpr the test."""

        # set up the point cloud
        self.radius = 0.5
        self.xyz, self.pt_type = [], []
        self._set_sphere_data()
        self._set_plane_data()
        self.xyz = np.array(self.xyz)
        self.point_cloud, npts = self._get_pc()

        # get the entire neighborhood
        self.neighbhorhood = list(range(npts))

        # theo val
        self.theoval = float(self.npt_plane) / npts

    def tearDown(self):
        pass


class TestPulsePenetratioFeatureExtractorRealData(unittest.TestCase):
    """Test the pulse extractor on real data and make sure it doesn't crash."""

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None
    targetpc = None
    cyl = None
    targetpc_index = None

    def test_valid(self):
        """Compute the echo ratio for a sphere/cylinder at different target points."""

        # read the data
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))

        # get the target point clouds
        random.seed(102938482634)
        self.targetpc = self._get_random_targets()
        self.targetpc_index = 0

        # volume descriptions
        radius = 0.5
        self.cyl = InfiniteCylinder(radius)
        cylinder_index = compute_neighborhoods(self.point_cloud, self.targetpc, self.cyl)

        # extractor
        extractor = PulsePenetrationFeatureExtractor()
        for index in cylinder_index:
            extractor.extract(self.point_cloud, index, None, None, None)

    def _get_random_targets(self):
        """Get a random target pc."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        return utils.copy_pointcloud(self.point_cloud, rand_indices)


if __name__ == '__main__':
    unittest.main()