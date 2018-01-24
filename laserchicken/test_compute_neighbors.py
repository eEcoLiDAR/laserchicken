# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:09:33 2018

@author: elena
"""

import os
import unittest
import random
from laserchicken import keys, compute_neighbors, read_las, utils


class TestComputeNeighbors(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    pointcloud = None

    def test_compute_neighbours(self):
       ''' Tetsing  computing of neighbors with KDtree '''
       num_all_pc_points = len(self.pointcloud[keys.point]["x"]["data"])
       rand_indices = [random.randint(0, num_all_pc_points) for p in range(5)]
       print("rand_indicies: ", rand_indices)

       target_pointcloud = utils.copy_pointcloud(self.pointcloud, rand_indices)
      # print("pointcloud: ", self.pointcloud)
       radius = 0.5

       compute_neighbors.compute_sphere_neighbourhoods(self.pointcloud, target_pointcloud, radius)
       raise Exception

    def setUp(self):
        self.pointcloud = read_las.read(os.path.join(self._test_data_source,self._test_file_name))

    def tearDown(self):
        pass
