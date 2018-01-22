from laserchicken.keys import *
import numpy as np
import datetime as dt


def generate_simple_test_point_cloud():
    pc = {point: {'x': {'type': 'float', 'data': [1, 2, 3]},
                  'y': {'type': 'float', 'data': [2, 3, 4]},
                  'z': {'type': 'float', 'data': [3, 4, 5]}}}
    return pc

def generate_complex_test_point_cloud():
    dto= dt.datetime(2018,1,18,16,1,0)
    pc = {point: {'x': {'type': 'float', 'data': [1, 2, 3, 4, 5]},
                  'y': {'type': 'float', 'data': [2, 3, 4, 5, 6]},
                  'z': {'type': 'float', 'data': [3, 4, 5, 6, 7]},
                  'return': {'type': 'int', 'data': np.array([1, 1, 2, 2, 1])}
                  },
          point_cloud: {'offset': {'type': 'double', 'data': 12.1}},
          provenance: [{'time' : dto , 'module' : 'filter'}]
         }
    return pc

def generate_simple_test_header():
    header = """ply
format ascii 1.0
element vertex 3
property float x
property float y
property float z
"""
    return  header
def generate_complex_test_header():
    header = """ply
format ascii 1.0
comment [
comment {'module': 'filter', 'time': datetime.datetime(2018, 1, 18, 16, 1)}
comment ]
element vertex 5
property float x
property float y
property float z
property int return
element pointcloud 1
property double offset
"""
    return  header
