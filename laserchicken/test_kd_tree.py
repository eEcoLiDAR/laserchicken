import os
import unittest

from laserchicken import keys,kd_tree,load


class TestKDTree(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    pointcloud = None

    def test_build_kd_tree(self):
        """ Should build kd tree without exception """
        kd_tree._build_kdtree(self.pointcloud)

    def test_kd_tree_cache(self):
        """ Tests the caching mechanism """
        firsttree = kd_tree.get_kdtree_for_pc(self.pointcloud)
        secondtree = kd_tree.get_kdtree_for_pc(self.pointcloud)
        self.assertEqual(firsttree,secondtree)

    def test_sphere_neighb_kd_tree(self):
        """ Tests whether sphere neighborhood gives good result """
        tree = kd_tree.get_kdtree_for_pc(self.pointcloud)
        rad = 10.
        point_index = 1000
        p = [self.pointcloud[keys.point]["x"]["data"][point_index],
             self.pointcloud[keys.point]["y"]["data"][point_index]]
        indices = tree.query_ball_point(p,rad)
        for i in indices:
            q = [self.pointcloud[keys.point]["x"]["data"][i],
                 self.pointcloud[keys.point]["y"]["data"][i]]
            self.assertTrue((p[0] - q[0])**2 + (p[1] - q[1])**2 < rad**2)



    def setUp(self):
        self.pointcloud = load(os.path.join(self._test_data_source,self._test_file_name))

    def tearDown(self):
        pass
