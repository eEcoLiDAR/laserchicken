import unittest

import numpy as np
from numpy.testing import assert_allclose

from laserchicken import keys
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.feature_extractor.normal_plane_feature_extractor import NormalPlaneFeatureExtractor


class TestNormalPlaneFeatureExtractor(unittest.TestCase):
    """Test the normal plane extractor."""

    pc = None
    neighborhood = None
    nvect = None

    def test_normal_plane(self):
        """Feature extractor finds correct normal vector and slope values for artificial data in a plane."""
        extractor = NormalPlaneFeatureExtractor()
        n1, n2, n3, slope_fit = extractor.extract(
            self.pc, self.neighborhood, None, None, None)
        assert_allclose(self.nvect, [n1[0], n2[0], n3[0]])
        assert_allclose(slope_fit, self.slope)

    def test_from_eigen(self):
        extractor = EigenValueVectorizeFeatureExtractor()
        n1, n2, n3, slope_fit = extractor.extract(
            self.pc, self.neighborhood, None, None, None)
        assert_allclose(self.nvect[0], n1[0])
        assert_allclose(self.nvect[1], n2[0])
        assert_allclose(self.nvect[2], n3[0])
        assert_allclose(slope_fit, self.slope)

    def setUp(self):
        """Set up of the test."""
        self.zaxis = np.array([0., 0., 1.])
        self.nvect = np.array([1., 2., 3.])
        self.nvect /= np.linalg.norm(self.nvect)
        self.slope = np.dot(self.nvect, self.zaxis)
        point = _generate_random_points_in_plane(self.nvect, npts=10)
        self.pc = {keys.point: {'x': {'type': 'double', 'data': point[:, 0]},
                                'y': {'type': 'double', 'data': point[:, 1]},
                                'z': {'type': 'double', 'data': point[:, 2]}}}
        self.neighborhood = [[3, 4, 5, 6, 7], [1, 2, 7, 8, 9], [1, 2, 7, 8, 9], [1, 2, 7, 8, 9], [1, 2, 7, 8, 9]]


def _generate_random_points_in_plane(nvect, dparam=0, npts=100, eps=0.0):
    """
    Generate a series of point all belonging to a plane.

    :param nvect: normal vector of the plane
    :param dparam: zero point value of the plane
    :param npts: number of points
    :param eps: std of the gaussian noise added to the z values of the planes
    :return: x,y,z coordinate of the points
    """
    np.random.seed(12345)
    a, b, c = nvect / np.linalg.norm(nvect)
    x, y = np.random.rand(npts), np.random.rand(npts)
    z = (dparam - a * x - b * y) / c
    if eps > 0:
        z += np.random.normal(loc=0., scale=eps, size=npts)
    return np.column_stack((x, y, z))


class EigenValueVectorizeFeatureExtractor(AbstractFeatureExtractor):
    is_vectorized = True

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['eigenv_1', 'eigenv_2', 'eigenv_3']

    @staticmethod
    def _get_cov(xyz):
        n = xyz.shape[2]
        m = xyz - xyz.sum(2, keepdims=1) / n
        return np.einsum('ijk,ilk->ijl', m, m) / (n - 1)

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        if not isinstance(neighborhood[0], list):
            neighborhood = [neighborhood]

        xyz_grp = get_xyz(sourcepc, neighborhood)
        cov_mat = self._get_cov(xyz_grp)
        eigval, eigvects = np.linalg.eig(cov_mat)
        print(eigvects)
        normals = eigvects[:, :, 2]
        print(normals)
        slope = np.dot(normals, np.array([0., 0., 1.]))
        return normals[:, 0], normals[:, 1], normals[:, 2], slope
        # return np.sort(eigval, axis=1)[:, ::-1]


def get_xyz(sourcepc, neighborhoods):
    """
    Get x, y, z tuple of one or more points in a point cloud.
    :param sourcepc:
    :param neighborhoods:
    :return:
    """
    xyz_grp = []
    for n in neighborhoods:
        x, y, z = get_point(sourcepc, n)
        xyz_grp.append(np.column_stack((x, y, z)).T)
    return np.array(xyz_grp)
