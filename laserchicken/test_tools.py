import numpy as np
from laserchicken.keys import point


def generate_test_point_cloud():
    pc = {point: {'x': {'type': 'double', 'data': np.array([1, 2, 3],dtype = np.float64)},
                  'y': {'type': 'double', 'data': np.array([2, 3, 4],dtype = np.float64)},
                  'z': {'type': 'double', 'data': np.array([3, 4, 5],dtype = np.float64)}}}
    return pc
