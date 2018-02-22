import os
import unittest
import pytest
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
        """Must pass as we provide everything needed."""

        # radius must be slightly larger than radius to avoid rounding error
        index_sphere = compute_neighborhoods(self.point_cloud, self.targetpc, Sphere(self.radius+1E-3))
        index_cyl = compute_neighborhoods(self.point_cloud, self.targetpc, InfiniteCylinder(self.radius+1E-3))
        indexes = [index_sphere[0],index_cyl[0]]

        extractor = EchoRatioFeatureExtractor()
        per = extractor.extract(self.point_cloud, indexes, None, None, None)

        self.assertTrue(np.allclose(per,self.theo_val))

    def test_invalid(self):
        """ Must raise TypeError as we do not provide correct indexes."""

        extractor = EchoRatioFeatureExtractor()
        with pytest.raises(TypeError):
            extractor.extract(self.point_cloud, [1,2,3], None,None,None)

    def _get_pc(self,xyz):
        return {keys.point: {'x': {'type': 'double', 'data': xyz[:, 0]},
                             'y': {'type': 'double', 'data': xyz[:, 1]},
                             'z': {'type': 'double', 'data': xyz[:, 2]}}}, len(xyz)

    def _set_sphere_data(self):
        """Create a sphere of point."""

        nteta,nphi = 11,11
        self.npt_sphere = nteta*nphi
        teta = np.linspace(0.1,2*np.pi,nteta)
        phi = np.linspace(0.1,np.pi,nphi)
        r = self.radius
        for t in teta:
            for p in phi:
                x = r * np.cos(t) * np.sin(p)
                y = r * np.sin(t) * np.sin(p)
                z = r * np.cos(p)
                self.xyz.append([x, y, z])


    def _set_cylinder_data(self):
        """Create a cylinder of point."""

        # nheight must be even so that the cylinder has no point
        # on the equator of the sphere
        nteta,nheight = 11,10
        self.npt_cyl = nteta*nheight
        r = self.radius
        teta = np.linspace(0.1, 2 * np.pi, nteta)
        height = np.linspace(-2*r, 2*r, nheight)

        for h in height:
            for t in teta:
                x,y,z = r * np.cos(t), r * np.sin(t), h
                self.xyz.append([x, y, z])


    def _get_central_point(self,index):
        """Get the central point."""
        return utils.copy_pointcloud(self.point_cloud, [index])


    def setUp(self):
        """
        Set up the test.

        Create a sphere and a cylinder of points and a central point
        The cylinder has no points on the equator of the sphere
        """

        # radius pf the cylinder and sphere
        self.radius = 0.5
        self.xyz = [[0.,0.,0.]]
        self._set_sphere_data()
        self._set_cylinder_data()
        self.point_cloud,self.npts = self._get_pc(np.array(self.xyz))
        self.targetpc = self._get_central_point(0)
        self.theo_val = (self.npt_sphere + 1) / (self.npt_sphere + self.npt_cyl + 1) * 100

    def tearDowm(self):
        """Tear it down."""
        pass


if __name__ == '__main__':
    unittest.main()