import os
import random
import unittest
import itertools
import numpy as np
import time

from laserchicken import compute_neighbors, feature_extractor, keys, read_las, utils
from laserchicken.volume_specification import InfiniteCylinder

from laserchicken.feature_extractor .eigenvals_feature_extractor import EigenValueFeatureExtractor, EigenValueVectorizeFeatureExtractor


class TestExtractEigenValues(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_eigenvalues_in_cylinders(self):
        """Test computing of eigenvalues in cylinder."""
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        target_point_cloud = utils.copy_pointcloud(self.point_cloud, rand_indices)
        n_targets = len(target_point_cloud[keys.point]["x"]["data"])
        radius = 2.5
        result_index_lists = compute_neighbors.compute_cylinder_neighborhood(
            self.point_cloud, target_point_cloud, radius)
        feature_extractor.compute_features(self.point_cloud, result_index_lists, target_point_cloud,
                                           ["eigenv_1", "eigenv_2", "eigenv_3"], InfiniteCylinder(5))
        for i in range(n_targets):
            lambda1, lambda2, lambda3 = utils.get_features(target_point_cloud, i, ["eigenv_1", "eigenv_2", "eigenv_3"])
            self.assertTrue(lambda1 >= lambda2 >= lambda3)
        self.assertEqual("laserchicken.feature_extractor.eigenvals_feature_extractor",
                         target_point_cloud[keys.provenance][0]["module"])

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass

class TestExtractEigenvaluesVector(unittest.TestCase):

    point_cloud = None

    def test_eig(self):
        """Test and compare the serial and vectorized eigenvalues."""

        # vectorized version
        t0 = time.time()
        extract_vect = EigenValueVectorizeFeatureExtractor()
        eigvals_vect = extract_vect.extract(self.point_cloud,self.neigh,None,None,None)
        print('Timing Vectorize : %f' %(time.time()-t0))

        # serial version
        eigvals = []
        t0 = time.time()
        for n in self.neigh:
            extract = EigenValueFeatureExtractor()
            eigvals.append(extract.extract(self.point_cloud,n,None,None,None))
        print('Timing Serial : %f' %(time.time()-t0))
        eigvals = np.array(eigvals)

        self.assertTrue(np.allclose(eigvals_vect,eigvals))
    def _get_index_cube(self,ix,iy,iz):
        ind = []

        for i in [ix-1,ix,ix+1]:
            for j in [iy-1,iy,iy+1]:
                for k in [iz-1,iz,iz+1]:
                    ind.append(i*self.dim**2+j*self.dim+k)
        return ind

    def _get_neighborhoods(self):
        neigh = []
        first = int(self.lengthcube/2)
        for ix in range(first,self.dim,self.lengthcube):
            for iy in range(first,self.dim,self.lengthcube):
                for iz in range(first,self.dim,self.lengthcube):
                    neigh.append(self._get_index_cube(ix,iy,iz))
        return neigh

    def setUp(self):

        self.ncube, self.lengthcube = 7,7
        self.dim = self.ncube*self.lengthcube
        x = np.linspace(-1,1,self.dim)
        x = np.random.rand(self.dim)
        pts_xyz = np.array(list(itertools.product(x,repeat=3)))
        self.point_cloud = {keys.point: {'x': {'type': 'double', 'data': pts_xyz[:, 0]},
                           'y': {'type': 'double', 'data': pts_xyz[:, 1]},
                           'z': {'type': 'double', 'data': pts_xyz[:, 2]}}}
        self.neigh = self._get_neighborhoods()


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()