# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:09:33 2018

@author: elena
"""

import os
import unittest
import random
import numpy as np
from laserchicken import keys, compute_neighbors, read_las, utils


class TestComputeNeighbors(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    pointcloud = None

    def test_compute_cylinder_neighbours(self):
       ''' Testing  computing of neighbors with KDtree '''
       num_all_pc_points = len(self.pointcloud[keys.point]["x"]["data"])
       rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]

       target_pointcloud = utils.copy_pointcloud(self.pointcloud, rand_indices)
       numtargets = len(target_pointcloud[keys.point]["x"]["data"])
       radius = 0.5
       resultpcs = compute_neighbors.compute_cylinder_neighbourhoods(self.pointcloud, target_pointcloud, radius)
       self.assertEqual(numtargets,len(resultpcs))
       for i in range(numtargets):
           targetx = target_pointcloud[keys.point]["x"]["data"][i]
           targety = target_pointcloud[keys.point]["y"]["data"][i]
           for j in range(len(resultpcs[i][keys.point]["x"]["data"])):
               nbptx = resultpcs[i][keys.point]["x"]["data"][j]
               nbpty = resultpcs[i][keys.point]["y"]["data"][j]
               dist = np.sqrt((nbptx - targetx)**2 + (nbpty - targety)**2)
               self.assertTrue(dist <= radius)


    def test_compute_sphere_neighbours(self):
       ''' Testing  computing of neighbors with KDtree '''
       num_all_pc_points = len(self.pointcloud[keys.point]["x"]["data"])
       rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]

       target_pointcloud = utils.copy_pointcloud(self.pointcloud, rand_indices)
       numtargets = len(target_pointcloud[keys.point]["x"]["data"])
       radius = 0.5
       resultpcs = compute_neighbors.compute_sphere_neighbourhoods(self.pointcloud, target_pointcloud, radius)
       self.assertEqual(numtargets,len(resultpcs))
       for i in range(numtargets):
           targetx,targety,targetz = utils.get_point(target_pointcloud,i)
           for j in range(len(resultpcs[i][keys.point]["x"]["data"])):
               nbptx,nbpty,nbptz = utils.get_point(resultpcs[i],j)
               dist = np.sqrt((nbptx - targetx)**2 + (nbpty - targety)**2 + (nbptz - targetz)**2)
               self.assertTrue(dist <= radius)

    def setUp(self):
        self.pointcloud = read_las.read(os.path.join(self._test_data_source,self._test_file_name))
        random.seed(102938482634)

    def tearDown(self):
        pass
