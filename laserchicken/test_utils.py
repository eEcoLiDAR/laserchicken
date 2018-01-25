import numpy as np
import unittest
import datetime
from laserchicken import utils,test_tools,keys

class TestUtils(unittest.TestCase):

    def test_GetPointCloudPoint(self):
        """ Should not raise exception. """
        pc = test_tools.generate_test_point_cloud()
        x,y,z = utils.get_point(pc,1)
        self.assertEqual(2,x)
        self.assertEqual(3,y)
        self.assertEqual(4,z)

    def test_CopyEmptyPointCloud(self):
        """ Should not raise exception. """
        pc = test_tools.generate_test_point_cloud()
        pc[keys.point]["x"]["data"] = np.array([])
        pc[keys.point]["y"]["data"] = np.array([])
        pc[keys.point]["z"]["data"] = np.array([])

        copypc = utils.copy_pointcloud(pc)
        self.assertEqual(0,len(copypc[keys.point]["x"]["data"]))


    def test_CopyNonEmptyPointCloud(self):
        """ Test whether coordinates are copied """
        pc = test_tools.generate_test_point_cloud()
        x = pc[keys.point]["x"]["data"]
        y = pc[keys.point]["y"]["data"]
        z = pc[keys.point]["z"]["data"]

        copypc = utils.copy_pointcloud(pc)
        self.assertTrue(all(x == copypc[keys.point]["x"]["data"]))
        self.assertTrue(all(y == copypc[keys.point]["y"]["data"]))
        self.assertTrue(all(z == copypc[keys.point]["z"]["data"]))


    def test_CopyPointCloudMetaData(self):
        """ Test whether metadata are copied """
        pc = test_tools.generate_test_point_cloud()
        pc["log"] = [{"time" : datetime.datetime(2018,1,23,12,15,59), "module" : "filter", "parameters" : [("z","gt",0.5)]}]

        copypc = utils.copy_pointcloud(pc)
        self.assertEqual(datetime.datetime(2018,1,23,12,15,59),copypc["log"][0]["time"])
        self.assertEqual("filter",copypc["log"][0]["module"])
        self.assertEqual([("z","gt",0.5)],copypc["log"][0]["parameters"])


    def test_CopyNonEmptyPointCloudBoolMask(self):
        """ Test whether coordinates are copied with boolean mask """
        pc = test_tools.generate_test_point_cloud()
        x = pc[keys.point]["x"]["data"][2]
        y = pc[keys.point]["y"]["data"][2]
        z = pc[keys.point]["z"]["data"][2]

        copypc = utils.copy_pointcloud(pc,array_mask = np.array([False,False,True]))
        self.assertTrue(all(np.array([x]) == copypc[keys.point]["x"]["data"]))
        self.assertTrue(all(np.array([y]) == copypc[keys.point]["y"]["data"]))
        self.assertTrue(all(np.array([z]) == copypc[keys.point]["z"]["data"]))


    def test_CopyNonEmptyPointCloudIntMask(self):
        """ Test whether coordinates are copied with array indexing """
        pc = test_tools.generate_test_point_cloud()
        x0,x1 = pc[keys.point]["x"]["data"][0],pc[keys.point]["x"]["data"][1]
        y0,y1 = pc[keys.point]["y"]["data"][0],pc[keys.point]["y"]["data"][1]
        z0,z1 = pc[keys.point]["z"]["data"][0],pc[keys.point]["z"]["data"][1]

        copypc = utils.copy_pointcloud(pc,array_mask = np.array([1,0]))
        self.assertTrue(all(np.array([x1,x0]) == copypc[keys.point]["x"]["data"]))
        self.assertTrue(all(np.array([y1,y0]) == copypc[keys.point]["y"]["data"]))
        self.assertTrue(all(np.array([z1,z0]) == copypc[keys.point]["z"]["data"]))
