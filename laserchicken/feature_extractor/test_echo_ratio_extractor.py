import os
import unittest
import itertools
import random
import numpy as np

from laserchicken import keys, read_las, utils
from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken.volume_specification import Sphere, InfiniteCylinder

from laserchicken.feature_extractor.echo_ratio_feature_extractor import EchoRatioFeatureExtractor


class TestEchoRatioFeatureExtractor(unittest.TestCase):
    """Test echo ratio extractor on artificial spherical data."""

    point_cloud = None
    targetpc = None

    def test_(self):

        index_sphere = compute_neighborhoods(self.point_cloud, self.targetpc, Sphere(self.radius))
        index_cyl = compute_neighborhoods(self.point_cloud, self.targetpc, InfiniteCylinder(self.radius))
        indexes = [index_sphere[0],index_cyl[0]]

        extractor = EchoRatioFeatureExtractor()
        per = extractor.extract(self.point_cloud, indexes, None, None, None)
        print(per)
        #self.assertTrue(np.allclose(per,test_values))

    def _get_data(self):
        """Create a 3D grid of equally spaved points."""

        x = np.linspace(-1, 1, 11)
        xyz = np.array([ list(p) for p in list(itertools.product(x,repeat=3))])
        return {keys.point: {'x': {'type': 'double', 'data': xyz[:, 0]},
                           'y': {'type': 'double', 'data': xyz[:, 1]},
                           'z': {'type': 'double', 'data': xyz[:, 2]}}},len(xyz)

    def _get_central_point(self):
        """Get the central point."""
        return utils.copy_pointcloud(self.point_cloud, [int(self.npts/2)])


    def setUp(self):
        """Set up the test."""

        self.point_cloud,self.npts = self._get_data()
        self.targetpc = self._get_central_point()
        self.radius = 0.5

    def tearDowm(self):
        """Tear it down."""
        pass


if __name__ == '__main__':
    unittest.main()