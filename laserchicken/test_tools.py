"""Collection of tools that can be used while testing the laserchicken software."""
import datetime as dt

import numpy as np

from laserchicken import keys


def generate_tiny_test_point_cloud():
    """Generate a simple but valid point cloud with 3 points."""
    pc = {keys.point: {'x': {'type': 'double', 'data': np.array([1, 2, 3], dtype=np.float64)},
                       'y': {'type': 'double', 'data': np.array([2, 3, 4], dtype=np.float64)},
                       'z': {'type': 'double', 'data': np.array([3, 4, 5], dtype=np.float64)}}}
    return pc


class SimpleTestData(object):
    """Test data within this class should all be in sync (reflect the same data)."""

    @staticmethod
    def get_point_cloud():
        """Get the point cloud data."""
        # This simple_test_point cloud and the simple_test_header should be in sync. Some tests depend on it.
        pc = {keys.point: {'x': {'type': 'double', 'data': np.array([1, 2, 3], dtype=np.float64)},
                           'y': {'type': 'double', 'data': np.array([20, 30, 40], dtype=np.float64)},
                           'z': {'type': 'double', 'data': np.array([300, 400, 500], dtype=np.float64)}}}
        return pc

    @staticmethod
    def get_header(is_binary=False):
        """Get the ply header."""
        if is_binary:
            format = "binary_little_endian"
        else:
            format = "ascii"
        # This simple_test_header cloud and the simple_test_point should be in sync. Some tests depend on it.
        header = """ply
format {} 1.0
element vertex 3
property double x
property double y
property double z
""".format(format)
        return header

    @staticmethod
    def get_data(is_binary=False):
        """Get the data in ply format."""
        if not is_binary:
            data = """1.0 20.0 300.0
2.0 30.0 400.0
3.0 40.0 500.0
"""
        else:
            with open("testdata/simple_test_data_little_endian.bin", "rb") as f:
                data = f.read().rstrip()
        return data


class ComplexTestData(object):
    """Test data within this class should all be in sync (reflect the same data)."""

    @staticmethod
    def get_point_cloud():
        """Get the point cloud data."""
        # This complex_test_point cloud and the complex_test_header should be in sync. Some tests depend on it.
        pc = {keys.point: {'x': {'type': 'double', 'data': np.array([1, 2, 3, 4, 5], dtype=np.float)},
                           'y': {'type': 'double', 'data': np.array([2, 3, 4, 5, 6], dtype=np.float)},
                           'z': {'type': 'double', 'data': np.array([3, 4, 5, 6, 7], dtype=np.float)},
                           'return': {'type': 'int', 'data': np.array([1, 1, 2, 2, 1], dtype=np.int32)}
                           },
              keys.point_cloud: {'offset': {'type': 'double', 'data': 12.1}},
              keys.provenance: [{"module": "filter", "time": str(dt.datetime(2018, 1, 18, 16, 1, 0))},
                                {"module": "filter", "time": str(dt.datetime(2018, 2, 4, 13, 11, 0))}]
              }
        return pc

    @staticmethod
    def get_header(is_binary=False):
        """Get the ply header."""
        if is_binary:
            format = "binary_little_endian"
        else:
            format = "ascii"
        # This complex_test_header cloud and the complex_test_point should be in sync. Some tests depend on it.
        header = ("""ply
format {} 1.0
comment [
comment {{"module": "filter", "time": "2018-01-18 16:01:00"}},
comment {{"module": "filter", "time": "2018-02-04 13:11:00"}}
comment ]
element vertex 5
property double x
property double y
property double z
property int return
element pointcloud 1
property double offset
""").format(format)
        return header

    @staticmethod
    def get_data(is_binary=False):
        """Get the data in ply format."""
        if not is_binary:
            data = """1.0 2.0 3.0 1
2.0 3.0 4.0 1
3.0 4.0 5.0 2
4.0 5.0 6.0 2
5.0 6.0 7.0 1
12.1
"""
        else:
            with open("testdata/complex_test_data_little_endian.bin", "rb") as f:
                data = f.read().rstrip()
        return data

    @staticmethod
    def get_wkt_polygon_around_first_point_only():
        """Get a polygon in wkt format that surrounds only the first point."""
        return "POLYGON(( 1.5 10.0, 1.5 -10.0, -1.5 -10.0, -1.5 1.0, 1.5 10.0 ))"


def create_point_cloud(x, y, z, normalized_z=None):
    """
    Create a point cloud object given only the x y z values.

    :param x: x attribute values
    :param y: y attribute values
    :param z: z attribute values
    :param normalized_z: optional normalized z attribute values
    :return: point cloud object
    """
    point_cloud = {keys.point: {'x': {'type': 'double', 'data': np.array(x, dtype=np.float)},
                                'y': {'type': 'double', 'data': np.array(y, dtype=np.float)},
                                'z': {'type': 'double', 'data': np.array(z, dtype=np.float)}},
                   keys.point_cloud: {},
                   keys.provenance: [{'time': (dt.datetime(2018, 1, 18, 16, 1, 0)), 'module': 'filter'}]}
    if normalized_z is not None:
        point_cloud[keys.point][keys.normalized_height] = {'type': 'double',
                                                           'data': np.array(normalized_z, dtype=np.float)}
    return point_cloud


def create_points_in_xy_grid(z_function):
    """Create 100 points in a grid of 10 by 10."""
    n_points = 100
    points = np.zeros((n_points, 3))
    for i in range(n_points):
        x = i % np.sqrt(n_points)
        y = np.floor(i / np.sqrt(n_points))
        points[i] = np.array((x, y, z_function(x, y)))
    return n_points, points
