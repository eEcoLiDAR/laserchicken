import numpy as np
import unittest
import datetime
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
        from laserchicken import select as somemodule
        utils.add_metadata(pc,somemodule,params = (0.5,"cylinder",4))
        self.assertEqual(len(pc[keys.provenance]),1)

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
