from laserchicken.keys import *
import numpy as np
import datetime as dt


def generate_simple_test_point_cloud():
    pc = {point: {'x': {'type': 'float', 'data': np.array([1, 2, 3])},
                  'y': {'type': 'float', 'data': np.array([20, 30, 40])},
                  'z': {'type': 'float', 'data': np.array([300, 400, 500])}}}
    return pc

def generate_complex_test_point_cloud():
    dto= dt.datetime(2018,1,18,16,1,0)
    pc = {point: {'x': {'type': 'float', 'data': np.array([1, 2, 3, 4, 5])},
                  'y': {'type': 'float', 'data': np.array([2, 3, 4, 5, 6])},
                  'z': {'type': 'float', 'data': np.array([3, 4, 5, 6, 7])},
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

def generate_simple_test_data():
    data = """1 20 300
2 30 400
3 40 500
"""
    return  data

def generate_complex_test_data():
    data = """1 2 3 1
2 3 4 1
3 4 5 2
4 5 6 2
5 6 7 1
12.1
"""
    return  data
