import itertools
import os
import random
import time
import unittest

import numpy as np

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils
from laserchicken.feature_extractor import EigenValueOld
from laserchicken.utils import copy_point_cloud
from .eigenvals_feature_extractor import EigenValueVectorizeFeatureExtractor
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import InfiniteCylinder


class TestExtractEigenValues(unittest.TestCase):
    def test_eigenvalues_in_cylinders(self):
        """Test computing provenance added (This should actually be part the general feature extractor test suite)."""
        random.seed(102938482634)
        point_cloud = read_las.read(
            os.path.join('testdata', 'AHN3.las'))
        num_all_pc_points = len(point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points)
                        for _ in range(20)]
        target_point_cloud = utils.copy_point_cloud(point_cloud, rand_indices)
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        radius = 2.5
        neighbors = compute_neighbors.compute_cylinder_neighborhood(
            point_cloud, target_point_cloud, radius)

        target_idx_base = 0
        for x in neighbors:
            feature_extractor.compute_features(point_cloud, x, target_idx_base, target_point_cloud,
                                               ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))
            target_idx_base += len(x)

        self.assertEqual("laserchicken.feature_extractor.eigenvals_feature_extractor",
                         target_point_cloud[keys.provenance][0]["module"])

    @staticmethod
    def test_eigenvalues_of_too_few_points_results_in_0():
        """If there are too few points to calculate the eigen values we output 0 (as opposed to NaN for example)."""
        a = np.array([5])
        pc = create_point_cloud(a, a, a)

        feature_extractor.compute_features(
            pc, [[0]], 0, pc, ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))

        eigen_val_123 = np.array(
            [pc[keys.point]['eigenv_{}'.format(i)]['data'] for i in [1, 2, 3]])
        np.testing.assert_allclose(eigen_val_123, np.zeros((3, 1)))

    def tearDown(self):
        pass


class TestExtractEigenvaluesVectorRealData(unittest.TestCase):
    point_cloud = None

    def test_eigen_multiple_neighborhoods(self):
        """
        Test and compare the serial and vectorized eigenvalues.

        Eigenvalues are computed for multiple cubic neighborhoods of points. A vectorized implementation and a serial
        implementation are compared and timed. Any difference in result between the two methods is definitely
        unexpected (except maybe in ordering of eigen values)
        """
        # vectorized version
        t0 = time.time()
        extract_vect = EigenValueVectorizeFeatureExtractor()
        eigvals_vect = extract_vect.extract(self.point_cloud, self.neigh, None, None, None)
        print('Timing Vectorize : {}'.format((time.time() - t0)))

        # serial version
        eigvals = []
        t0 = time.time()
        for n in self.neigh:
            extract = EigenValueOld()
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
        _PC_260807 = read_las.read(os.path.join(_TEST_DATA_SOURCE, _TEST_FILE_NAME))
        _PC_1000 = copy_point_cloud(_PC_260807, array_mask=(
            np.random.choice(range(len(_PC_260807[keys.point]['x']['data'])), size=1000, replace=False)))
        _1000_NEIGHBORHOODS_IN_260807 = next(compute_neighbors.compute_neighborhoods(_PC_260807, _PC_1000, _CYLINDER))

        self.point_cloud = _PC_260807
        self.neigh = _1000_NEIGHBORHOODS_IN_260807
