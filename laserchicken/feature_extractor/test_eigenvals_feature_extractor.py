import os
import random
import time
import unittest

import numpy as np

from laserchicken import compute_neighbors, keys, load, utils
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.feature_extractor.feature_extraction import compute_features
from laserchicken.test_tools import create_point_cloud
from laserchicken.utils import copy_point_cloud
from laserchicken.volume_specification import InfiniteCylinder
from .eigenvals_feature_extractor import EigenValueVectorizeFeatureExtractor


class TestExtractEigenValues(unittest.TestCase):
    def test_eigenvalues_in_cylinders(self):
        """Test provenance added (This should actually be part the general feature extractor test suite)."""
        random.seed(102938482634)
        point_cloud = load(os.path.join('testdata', 'AHN3.las'))
        num_all_pc_points = len(point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for _ in range(20)]
        target_point_cloud = utils.copy_point_cloud(point_cloud, rand_indices)
        radius = 2.5
        neighbors = compute_neighbors.compute_cylinder_neighborhood(point_cloud, target_point_cloud, radius)

        compute_features(point_cloud, neighbors, target_point_cloud,
                         ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))

        self.assertEqual("laserchicken.feature_extractor.eigenvals_feature_extractor",
                         target_point_cloud[keys.provenance][-1]["module"])

    @staticmethod
    def test_eigenvalues_of_too_few_points_results_in_0():
        """If there are too few points to calculate the eigen values don't output NaN or inf."""
        a = np.array([5])
        pc = create_point_cloud(a, a, a)

        compute_features(pc, [[0]], pc, ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))

        eigen_val_123 = np.array([pc[keys.point]['eigenv_{}'.format(i)]['data'] for i in [1, 2, 3]])
        assert not np.any(np.isnan(eigen_val_123))
        assert not np.any(np.isinf(eigen_val_123))


class TestExtractEigenvaluesComparison(unittest.TestCase):
    point_cloud = None

    def test_eigen_multiple_neighborhoods(self):
        """
        Test and compare the serial and vectorized eigenvalues.

        Eigenvalues are computed for a list of neighborhoods in real data. A vectorized implementation and a serial
        implementation are compared and timed. Any difference in result between the two methods is definitely
        unexpected (except maybe in ordering of eigen values).
        """
        # vectorized version
        t0 = time.time()
        extract_vect = EigenValueVectorizeFeatureExtractor()
        eigvals_vect = extract_vect.extract(self.point_cloud, self.neigh, None, None, None)
        print('Timing Vectorize : {}'.format((time.time() - t0)))
        eigvals_vect = np.vstack(eigvals_vect[:3]).T

        # serial version
        eigvals = []
        t0 = time.time()
        for n in self.neigh:
            extract = EigenValueSerial()
            eigvals.append(extract.extract(self.point_cloud, n, None, None, None))
        print('Timing Serial : {}'.format((time.time() - t0)))
        eigvals = np.array(eigvals)

        np.testing.assert_allclose(eigvals_vect, eigvals)

    def setUp(self):
        """
        Set up the test.

        Load in a bunch of real data from AHN3.
        """
        np.random.seed(1234)

        _TEST_FILE_NAME = 'AHN3.las'
        _TEST_DATA_SOURCE = 'testdata'

        _CYLINDER = InfiniteCylinder(4)
        _PC_260807 = load(os.path.join(_TEST_DATA_SOURCE, _TEST_FILE_NAME))
        _PC_1000 = copy_point_cloud(_PC_260807, array_mask=(
            np.random.choice(range(len(_PC_260807[keys.point]['x']['data'])), size=1000, replace=False)))
        _1000_NEIGHBORHOODS_IN_260807 = list(compute_neighbors.compute_neighborhoods(_PC_260807, _PC_1000, _CYLINDER))

        self.point_cloud = _PC_260807
        self.neigh = _1000_NEIGHBORHOODS_IN_260807


class TestExtractNormalPlaneArtificialData0(unittest.TestCase):
    def test_regression(self):
        n_x = 3
        slope_ = 1.0
        x_, y_ = np.meshgrid(range(n_x), range(n_x))
        x = x_.flatten()
        y = y_.flatten()
        z = [slope_ * x[i] for i in range(len(x))]

        dim = (1, 3, len(x))
        mask = np.zeros(dim)
        xyz_grp = np.ma.MaskedArray(np.zeros(dim), mask == 0)
        xyz_grp[0, 0, :] = x
        xyz_grp[0, 1, :] = y
        xyz_grp[0, 2, :] = z

        point_cloud = create_point_cloud(xyz_grp[0, 0, :], xyz_grp[0, 1, :], xyz_grp[0, 2, :])
        extractor = EigenValueVectorizeFeatureExtractor()
        neighborhoods = [list(range(len(x)))]
        normals = np.array(extractor.extract(point_cloud, neighborhoods, point_cloud, None, None)[3:6])[:, 0]
        np.testing.assert_allclose(normals, np.array((-np.sqrt(2) / 2, 0, np.sqrt(2) / 2)))

    def test_from_eigen(self):
        nvect = np.array([1., 2., 3.])
        neighborhood, pc = create_point_cloud_in_plane_and_neighborhood(nvect)
        extractor = EigenValueVectorizeFeatureExtractor()

        n1, n2, n3, slope_fit = extractor.extract(pc, neighborhood, None, None, None)[3:]

        np.testing.assert_allclose(nvect[0], n1[0])
        np.testing.assert_allclose(nvect[1], n2[0])
        np.testing.assert_allclose(nvect[2], n3[0])

    def test_normal_always_up(self):
        """Tests whether resulting normals are always pointing upwards (positive z component). As this should happen
        by chance a lot already, we test many times to make sure results are positive consistently."""
        z_of_normals = []
        for i in range(100):
            neighborhood, pc = create_point_cloud_in_plane_and_neighborhood()
            z_of_normals += list(EigenValueVectorizeFeatureExtractor().extract(pc, neighborhood, None, None, None)[5])
        np.testing.assert_array_less(np.zeros_like(z_of_normals), z_of_normals)

    def test_normal_unit_length(self):
        """Tests whether resulting normals are unit length"""
        neighborhood, pc = create_point_cloud_in_plane_and_neighborhood()
        normals = np.array(EigenValueVectorizeFeatureExtractor().extract(pc, neighborhood, None, None, None)[3:6])
        lengths = np.sum(normals * normals, axis=0)
        np.testing.assert_almost_equal(np.ones_like(lengths), lengths)


class TestExtractSlopeArtificialData(unittest.TestCase):
    def test_positive_slope(self):
        """Tests whether resulting slopes are always positive. As this should happen
        by chance a lot already, we test many times to make sure results are positive consistently."""
        slopes = []
        for i in range(100):
            neighborhood, pc = create_point_cloud_in_plane_and_neighborhood()
            slopes += list(EigenValueVectorizeFeatureExtractor().extract(pc, neighborhood, None, None, None)[6])
        np.testing.assert_array_less(np.zeros_like(slopes), slopes)

    def test_001_has_slope_0(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 0., 1.]), 0.)

    def test_011_has_slope_1(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 1., 1.]), 1.)

    def test_01min1_has_slope_1(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 1., -1.]), 1.)

    def test_0min11_has_slope_1(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., -1., 1.]), 1.)

    def test_00251_has_slope_025(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 0.25, 1.]), 0.25)

    def test_021_has_slope_2(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 2., 1.]), 2.)

    def test_031_has_slope_3(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 3., 1.]), 3.)

    def test_0205_has_slope_4(self):
        self.assert_data_with_normal_vector_has_slope(np.array([0., 2., 0.5]), 4.)

    @staticmethod
    def assert_data_with_normal_vector_has_slope(nvect, expected_slope):
        """Create random point cloud with normal vector nvect and assert that estimated slope has expected value."""
        neighborhood, pc = create_point_cloud_in_plane_and_neighborhood(nvect)
        extractor = EigenValueVectorizeFeatureExtractor()
        slope = extractor.extract(pc, neighborhood, None, None, None)[6]
        np.testing.assert_allclose(slope, expected_slope, atol=1e-6)


def create_point_cloud_in_plane_and_neighborhood(nvect=None):
    if nvect is None:
        nvect = np.random.randn(3)

    nvect /= np.linalg.norm(nvect)
    points = _generate_random_points_in_plane(nvect, dparam=0, npts=100)
    neighborhood, pc = create_point_cloud_and_neighborhoods(points)
    return neighborhood, pc


def create_point_cloud_and_neighborhoods(point):
    pc = {keys.point: {'x': {'type': 'double', 'data': point[:, 0]},
                       'y': {'type': 'double', 'data': point[:, 1]},
                       'z': {'type': 'double', 'data': point[:, 2]}}}
    neighborhood = [[3, 4, 5, 6, 7], [1, 2, 7, 8, 9], [1, 7, 8, 9], [1, 2, 7, 9], [2, 7, 8, 9]]
    return neighborhood, pc


def _generate_random_points_in_plane(nvect, dparam, npts, eps=0.0):
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


class EigenValueSerial(FeatureExtractor):
    """Old serial implementation. Used to test the current (vectorized) implementation against."""

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ["eigenv_1", "eigenv_2", "eigenv_3"]

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        nbptsX, nbptsY, nbptsZ = utils.get_point(sourcepc, neighborhood)
        matrix = np.column_stack((nbptsX, nbptsY, nbptsZ))

        try:
            eigenvals, eigenvecs = self._structure_tensor(matrix)
        except ValueError as err:
            if str(err) == 'Not enough points to compute eigenvalues/vectors.':
                return [0, 0, 0]
            else:
                raise

        return [eigenvals[0], eigenvals[1], eigenvals[2]]

    @staticmethod
    def _structure_tensor(points):
        """
        Computes the structure tensor of points by computing the eigenvalues
        and eigenvectors of the covariance matrix of a point cloud.
        Parameters
        ----------
        points : (Mx3) array
            X, Y and Z coordinates of points.
        Returns
        -------
        eigenvalues : (1x3) array
            The eigenvalues corresponding to the eigenvectors of the covariance
            matrix.
        eigenvectors : (3,3) array
            The eigenvectors of the covariance matrix.
        """
        if points.shape[0] > 3:
            cov_mat = np.cov(points, rowvar=False)
            eigenvalues, eigenvectors = np.linalg.eig(cov_mat)
            order = np.argsort(-eigenvalues)
            eigenvalues = eigenvalues[order]
            eigenvectors = eigenvectors[:, order]
            return eigenvalues, eigenvectors
        else:
            raise ValueError('Not enough points to compute eigenvalues/vectors.')
