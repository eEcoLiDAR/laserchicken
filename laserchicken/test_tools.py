import numpy as np
import datetime as dt
from laserchicken import keys


def generate_test_point_cloud():
    pc = {keys.point: {'x': {'type': 'double', 'data': np.array([1, 2, 3], dtype=np.float64)},
                       'y': {'type': 'double', 'data': np.array([2, 3, 4], dtype=np.float64)},
                       'z': {'type': 'double', 'data': np.array([3, 4, 5], dtype=np.float64)}}}
    return pc


class SimpleTestData(object):
    """ Test data within this class should all be in sync (reflect the same data)."""

    @staticmethod
    def get_point_cloud():
        # This simple_test_point cloud and the simple_test_header should be in sync. Some tests depend on it.
        pc = {keys.point: {'x': {'type': 'float', 'data': np.array([1, 2, 3])},
                           'y': {'type': 'float', 'data': np.array([20, 30, 40])},
                           'z': {'type': 'float', 'data': np.array([300, 400, 500])}}}
        return pc

    @staticmethod
    def get_header():
        # This simple_test_header cloud and the simple_test_point should be in sync. Some tests depend on it.
        header = """ply
format ascii 1.0
element vertex 3
property float x
property float y
property float z
"""
        return header

    @staticmethod
    def get_data():
        data = """1 20 300
2 30 400
3 40 500
"""
        return data


class ComplexTestData(object):
    """ Test data within this class should all be in sync (reflect the same data)."""

    @staticmethod
    def get_point_cloud():
        # This complex_test_point cloud and the complex_test_header should be in sync. Some tests depend on it.
        pc = {keys.point: {'x': {'type': 'float', 'data': np.array([1, 2, 3, 4, 5])},
                           'y': {'type': 'float', 'data': np.array([2, 3, 4, 5, 6])},
                           'z': {'type': 'float', 'data': np.array([3, 4, 5, 6, 7])},
                           'return': {'type': 'int', 'data': np.array([1, 1, 2, 2, 1])}
                           },
              keys.point_cloud: {'offset': {'type': 'double', 'data': 12.1}},
              keys.provenance: [{'time': (dt.datetime(2018, 1, 18, 16, 1, 0)), 'module': 'filter'}]
              }
        return pc

    @staticmethod
    def get_header():
        # This complex_test_header cloud and the complex_test_point should be in sync. Some tests depend on it.
        comment = {"module": "filter", "time": str(dt.datetime(2018, 1, 18, 16, 1, 0))}
        header = """ply
format ascii 1.0
comment [
comment %s
comment ]
element vertex 5
property float x
property float y
property float z
property int return
element pointcloud 1
property double offset
""" % str(comment)
        return header

    @staticmethod
    def get_data():
        data = """1 2 3 1
2 3 4 1
3 4 5 2
4 5 6 2
5 6 7 1
12.1
"""
        return data

    @staticmethod
    def get_wkt_polygon_around_first_point_only():
        return "POLYGON(( 1.5 10.0, 1.5 -10.0, -1.5 -10.0, -1.5 1.0, 1.5 10.0 ))"


def create_point_cloud(x, y, z):
    """
    Create a point cloud object given only the x y z values
    :param x: x attribute values
    :param y: y attribute values
    :param z: z attribute values
    :return: point cloud object
    """
    return {keys.point: {'x': {'type': 'float', 'data': np.array(x)},
                         'y': {'type': 'float', 'data': np.array(y)},
                         'z': {'type': 'float', 'data': np.array(z)}},
            keys.point_cloud: {},
            keys.provenance: [{'time': (dt.datetime(2018, 1, 18, 16, 1, 0)), 'module': 'filter'}]
            }
