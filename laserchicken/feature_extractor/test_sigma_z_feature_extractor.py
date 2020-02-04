import os
import time
import unittest

import numpy as np
from numpy.linalg import LinAlgError

from laserchicken import compute_neighbors, keys, read_las
from laserchicken.feature_extractor import compute_features
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.test_tools import create_point_cloud, create_points_in_xy_grid
from laserchicken.utils import get_point, fit_plane, copy_point_cloud
from laserchicken.volume_specification import InfiniteCylinder
from .sigma_z_feature_extractor import SigmaZFeatureExtractor as SigmaZVectorizedFeatureExtractor

class TestExtractSigmaZ(unittest.TestCase):
    def test_constantValues_result0(self):
        def z_constant(x, y):
            return 2

        assert_std_for_z_function_in_xy_grid(z_constant, 0)

    def test_checkered1sAnd0s_resultHalf(self):
        """Standard deviation of checker pattern of 0s and 1s should be 0.5"""

        def z_checkered(x, y):
            return ((x + y) % 2) + 2

        assert_std_for_z_function_in_xy_grid(z_checkered, 0.5)

    def test_checkered1sAnd0sPlusSkewed_resultHalf(self):
        """Standard deviation of checker pattern of 0s and 1s should be 0.5, adding a plane should not change that"""

        def z_checkered(x, y):
            return ((x + y) % 2) + 2 + x + y

        assert_std_for_z_function_in_xy_grid(z_checkered, 0.5)


def assert_std_for_z_function_in_xy_grid(z_checkered, expected):
    """Assert that the standard deviation of z values in a grid of unit x and y"""
    n_points, points = create_points_in_xy_grid(z_checkered)
    point_cloud = create_point_cloud(points[:, 0], points[:, 1], points[:, 2])
    targets = create_point_cloud([0], [0], [0])
    compute_features(point_cloud, [range(n_points)], 0, targets, [
                     'sigma_z'], InfiniteCylinder(10))
    np.testing.assert_almost_equal(
        targets[keys.point]['sigma_z']['data'][0], expected)

class TestExtractSigmaZComparison(unittest.TestCase):
    point_cloud = None

    def test_sigma_z_multiple_neighborhoods(self):
        """
        Test and compare the serial and vectorized sigma_z implementations.

        sigma_z is computed for a list of neighborhoods in real data. A vectorized implementation and a serial
        implementation are compared and timed. Any difference in result between the two methods is definitely
        unexpected.
        """
        # vectorized version
        t0 = time.time()
        extract_vect = SigmaZVectorizedFeatureExtractor()
        sigma_z_vec = extract_vect.extract(self.point_cloud, self.neigh, None, None, None)
        print('Timing Vectorize : {}'.format((time.time() - t0)))

        # serial version
        sigma_z = []
        t0 = time.time()
        for n in self.neigh:
            extract = SigmaZSerial()
            sigma_z.append(extract.extract(self.point_cloud, n, None, None, None))
        print('Timing Serial : {}'.format((time.time() - t0)))
        sigma_z = np.array(sigma_z)
        np.testing.assert_allclose(sigma_z_vec, sigma_z, atol=1.e-7)

    def setUp(self):
        """
        Set up the test.

        Load in a bunch of real data from AHN3.
        """
        np.random.seed(1234)

        _TEST_FILE_NAME = 'AHN3.las'
        _TEST_DATA_SOURCE = 'testdata'

        _CYLINDER = InfiniteCylinder(4)
        _PC_260807 = read_las.read(os.path.join(_TEST_DATA_SOURCE, _TEST_FILE_NAME))
        _PC_1000 = copy_point_cloud(_PC_260807, array_mask=(
            np.random.choice(range(len(_PC_260807[keys.point]['x']['data'])), size=1000, replace=False)))
        _1000_NEIGHBORHOODS_IN_260807 = next(compute_neighbors.compute_neighborhoods(_PC_260807, _PC_1000, _CYLINDER))

        self.point_cloud = _PC_260807
        self.neigh = _1000_NEIGHBORHOODS_IN_260807

class SigmaZSerial(FeatureExtractor):
    """Serial implementation. Used to test the current (vectorized) implementation."""

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ["sigma_z"]

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        x, y, z = get_point(sourcepc, neighborhood)
        try:
            plane_estimator, residuals = fit_plane(x, y, z)
            return np.sqrt(np.divide(residuals, x.size))
        except LinAlgError:
            return 0
