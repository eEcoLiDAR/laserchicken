import numpy as np
import unittest
import datetime
import pytest
from laserchicken import utils, test_tools, keys
from laserchicken.utils import fit_plane
from time import time

class TestUtils(unittest.TestCase):
    def test_GetPointCloudPoint(self):
        """ Should not raise exception. """
        pc = test_tools.generate_tiny_test_point_cloud()
        x, y, z = utils.get_point(pc, 1)
        self.assertEqual(2, x)
        self.assertEqual(3, y)
        self.assertEqual(4, z)

    def test_GetPointCloudPointFeature(self):
        """ Should not raise exception. """
        pc = test_tools.generate_tiny_test_point_cloud()
        cols = 0.5 * (pc[keys.point]["x"]["data"] + pc[keys.point]["y"]["data"])
        pc[keys.point]["color"] = {"type": "double", "data": cols}
        x, y, z = utils.get_point(pc, 1)
        c = utils.get_attribute_value(pc, 1, "color")
        self.assertEqual(c, 0.5 * (x + y))

    def test_GetPointCloudPointFeatures(self):
        """ Should not raise exception. """
        pc = test_tools.generate_tiny_test_point_cloud()
        cols = 0.5 * (pc[keys.point]["x"]["data"] + pc[keys.point]["y"]["data"])
        flavs = 0.5 * (pc[keys.point]["x"]["data"] - pc[keys.point]["y"]["data"])
        pc[keys.point]["color"] = {"type": "double", "data": cols}
        pc[keys.point]["flavor"] = {"type": "double", "data": flavs}
        x, y, z = utils.get_point(pc, 2)
        c, f = utils.get_features(pc, ("color", "flavor"), 2)
        self.assertEqual(c, 0.5 * (x + y))
        self.assertEqual(f, 0.5 * (x - y))

    def test_CopyEmptyPointCloud(self):
        """ Should not raise exception. """
        pc = test_tools.generate_tiny_test_point_cloud()
        pc[keys.point]["x"]["data"] = np.array([])
        pc[keys.point]["y"]["data"] = np.array([])
        pc[keys.point]["z"]["data"] = np.array([])

        copypc = utils.copy_point_cloud(pc)
        self.assertEqual(0, len(copypc[keys.point]["x"]["data"]))

    def test_CopyNonEmptyPointCloud(self):
        """ Test whether coordinates are copied """
        pc = test_tools.generate_tiny_test_point_cloud()
        x = pc[keys.point]["x"]["data"]
        y = pc[keys.point]["y"]["data"]
        z = pc[keys.point]["z"]["data"]

        copypc = utils.copy_point_cloud(pc)
        self.assertTrue(all(x == copypc[keys.point]["x"]["data"]))
        self.assertTrue(all(y == copypc[keys.point]["y"]["data"]))
        self.assertTrue(all(z == copypc[keys.point]["z"]["data"]))

    def test_CopyPointCloudMetaData(self):
        """ Test whether metadata are copied """
        pc = test_tools.generate_tiny_test_point_cloud()
        pc["log"] = [
            {"time": datetime.datetime(2018, 1, 23, 12, 15, 59), "module": "filter", "parameters": [("z", "gt", 0.5)]}]

        copypc = utils.copy_point_cloud(pc)
        self.assertEqual(datetime.datetime(2018, 1, 23, 12, 15, 59), copypc["log"][0]["time"])
        self.assertEqual("filter", copypc["log"][0]["module"])
        self.assertEqual([("z", "gt", 0.5)], copypc["log"][0]["parameters"])

    def test_CopyNonEmptyPointCloudBoolMask(self):
        """ Test whether coordinates are copied with boolean mask """
        pc = test_tools.generate_tiny_test_point_cloud()
        x = pc[keys.point]["x"]["data"][2]
        y = pc[keys.point]["y"]["data"][2]
        z = pc[keys.point]["z"]["data"][2]

        copypc = utils.copy_point_cloud(pc, array_mask=np.array([False, False, True]))
        self.assertTrue(all(np.array([x]) == copypc[keys.point]["x"]["data"]))
        self.assertTrue(all(np.array([y]) == copypc[keys.point]["y"]["data"]))
        self.assertTrue(all(np.array([z]) == copypc[keys.point]["z"]["data"]))

    def test_CopyNonEmptyPointCloudIntMask(self):
        """ Test whether coordinates are copied with array indexing """
        pc = test_tools.generate_tiny_test_point_cloud()
        x0, x1 = pc[keys.point]["x"]["data"][0], pc[keys.point]["x"]["data"][1]
        y0, y1 = pc[keys.point]["y"]["data"][0], pc[keys.point]["y"]["data"][1]
        z0, z1 = pc[keys.point]["z"]["data"][0], pc[keys.point]["z"]["data"][1]

        copypc = utils.copy_point_cloud(pc, array_mask=np.array([1, 0]))
        self.assertTrue(all(np.array([x1, x0]) == copypc[keys.point]["x"]["data"]))
        self.assertTrue(all(np.array([y1, y0]) == copypc[keys.point]["y"]["data"]))
        self.assertTrue(all(np.array([z1, z0]) == copypc[keys.point]["z"]["data"]))

    def test_AddMetaDataToPointCloud(self):
        """ Test adding info to the point cloud for test module """
        pc = test_tools.generate_tiny_test_point_cloud()
        from laserchicken import filter as somemodule
        utils.add_metadata(pc,somemodule,params = (0.5,"cylinder",4))
        self.assertEqual(len(pc[keys.provenance]),1)

    def test_AddToPointCloudEmpty(self):
        pc_1 = utils.create_point_cloud([],[],[])
        pc_2 = test_tools.generate_tiny_test_point_cloud()
        utils.add_to_point_cloud(pc_1, pc_2)
        for attr in pc_2[keys.point].keys():
            self.assertIn(attr, pc_1[keys.point])
            self.assertEqual(pc_1[keys.point][attr]['type'],
                             pc_2[keys.point][attr]['type'])
            self.assertTrue(all(pc_1[keys.point][attr]['data'] == pc_2[keys.point][attr]['data']))

    def test_AddToPointCloudInvalid(self):
        pc_1 = test_tools.SimpleTestData.get_point_cloud()
        # invalid format
        pc_2 = {}
        with pytest.raises(TypeError):
            utils.add_to_point_cloud(pc_1, pc_2)
        with pytest.raises(AttributeError):
            utils.add_to_point_cloud(pc_2, pc_1)
        # non-matching attributes
        test_data = test_tools.ComplexTestData()
        pc_2 = test_data.get_point_cloud()
        with pytest.raises(AttributeError):
            utils.add_to_point_cloud(pc_1, pc_2)
        # different structure
        pc_2 = {'vertex':{'x':1, 'y':2, 'z':3}}
        with pytest.raises(TypeError):
            utils.add_to_point_cloud(pc_1, pc_2)
        # different data types
        pc_2 = {'vertex': {'x': {'data': np.zeros(3, dtype=int), 'type': 'int'},
                           'y': {'data': np.zeros(3, dtype=int), 'type': 'int'},
                           'z': {'data': np.zeros(3, dtype=int), 'type': 'int'}}}
        with pytest.raises(ValueError):
            utils.add_to_point_cloud(pc_1, pc_2)

    def test_AddToPointCloud(self):
        test_data = test_tools.ComplexTestData()
        pc_source = test_data.get_point_cloud()
        pc_dest = utils.copy_point_cloud(pc_source)
        utils.add_to_point_cloud(pc_dest, pc_source)
        for key in pc_source.keys():
            self.assertIn(key, pc_dest)
        for attr in pc_source[keys.point].keys():
            self.assertEqual(len(pc_dest[keys.point][attr]['data']),
                             2*len(pc_source[keys.point][attr]['data']))
        self.assertEqual(pc_dest[keys.provenance][-1]['module'],
                         'laserchicken.utils')
    
    def test_AddFeatureArray(self):
        test_data = test_tools.ComplexTestData()
        pc = test_data.get_point_cloud()
        feature_add = np.array([1, 1, 1, 1, 1], dtype=int)
        utils.update_feature(pc, 'test_feature', feature_add)
        self.assertIn('test_feature', pc[keys.point])
        self.assertTrue(all(pc[keys.point]['test_feature']['data'] == feature_add))

    def test_AddFeatureArrayInvalid(self):
        test_data = test_tools.ComplexTestData()
        pc = test_data.get_point_cloud()
        feature_add = np.array([1, 1, 1, 1, 1, 2], dtype=int)
        with pytest.raises(AssertionError):
            utils.update_feature(pc, 'test_feature', feature_add)
    
    def test_AddFeatureArrayMask(self):
        test_data = test_tools.ComplexTestData()
        pc = test_data.get_point_cloud()
        feature_add = np.array([1, 2, 3, 4], dtype=int)
        mask = np.array([1, 1, 0, 1, 1], dtype=bool)
        utils.update_feature(pc, 'test_feature', feature_add, array_mask=mask)
        self.assertIn('test_feature', pc[keys.point])
        self.assertTrue(all(pc[keys.point]['test_feature']['data'] == [1, 2, 0, 3, 4]))
    
    def test_AddFeatureArrayMaskInvalid(self):
        test_data = test_tools.ComplexTestData()
        pc = test_data.get_point_cloud()
        feature_add = np.array([1, 2, 3, 4], dtype=int)
        mask = np.array([1, 1, 1, 1, 1], dtype=bool)
        with pytest.raises(AssertionError):
            utils.update_feature(pc, 'test_feature', feature_add, array_mask=mask)

    def test_AddFeatureValueMask(self):
        test_data = test_tools.ComplexTestData()
        pc = test_data.get_point_cloud()
        feature_add = 1.1
        mask = np.array([1, 1, 0, 1, 1], dtype=bool)
        utils.update_feature(pc, 'test_feature', feature_add, array_mask=mask)
        self.assertIn('test_feature', pc[keys.point])
        self.assertTrue(all(pc[keys.point]['test_feature']['data'] == [1.1, 1.1, 0.0, 1.1, 1.1]))
    
    def test_AddFeatureValueMaskInvalid(self):
        test_data = test_tools.ComplexTestData()
        pc = test_data.get_point_cloud()
        feature_add = 1.1
        mask = np.array([1, 1, 0, 1, 1, 1], dtype=bool)
        with pytest.raises(AssertionError):
            utils.update_feature(pc, 'test_feature', feature_add, array_mask=mask)
        

        

class TestPlaneFit(unittest.TestCase):

    def test_leastsqr(self):
        # n_points = 100
        # points = np.zeros((n_points, 3))
        # for i in range(n_points):
        #     z = 5 + i % np.sqrt(n_points)
        #     points[i] = np.array(((i % np.sqrt(n_points)), (np.floor(i / np.sqrt(n_points))), z))
        #t0 = time()
        f = fit_plane(self.points[:, 0], self.points[:, 1], self.points[:, 2])
        #print('LSQR : %f' %(time()-t0))
        estimates = f(self.points[:, 0], self.points[:, 1])
        np.testing.assert_allclose(estimates, self.points[:, 2])


    def test_FitPlaneSVD(self):
        """Test the normal vector extraction with SVD."""
        #t0 = time()
        nfit = utils.fit_plane_svd(self.points[:,0], self.points[:,1], self.points[:,2])
        #print('SVD  : %f' %(time()-t0))
        self.assertTrue(np.allclose(nfit, self.n))


    def generate_random_points_inplane(self,nvect, dparam=0, npts=100, eps=0.0):
        """
        Generate a series of point all belonging to a plane.

        :param nvect: normal vector of the plane
        :param dparam: zero point value of the plane
        :param npts: number of points
        :param eps: std of the gaussian noise added to the z values of the planes
        :return: x,y,z coordinate of the points
        """
        a, b, c = nvect / np.linalg.norm(nvect)
        x, y = np.random.rand(npts), np.random.rand(npts)
        z = (dparam - a * x - b * y) / c
        if eps > 0:
            z += np.random.normal(loc=0., scale=eps, size=npts)
        return np.column_stack((x, y, z))


    def setUp(self):
        """Set up the data points."""

        self.n = np.array([1., 2., 3.])
        self.n /= np.linalg.norm(self.n)
        self.points = self.generate_random_points_inplane(self.n,eps=0)

    def tearDown(self):
        """Tear it down."""
        pass

if __name__ == '__main__':
    unittest.main()
