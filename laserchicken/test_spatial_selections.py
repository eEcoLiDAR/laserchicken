import unittest
import pytest

import numpy as np
import pandas as pd

from laserchicken.keys import point
from laserchicken import read_las
from laserchicken.spatial_selections import points_in_polygon_wkt, points_in_polygon_shp

class TestSpatialSelectionWKT(unittest.TestCase):
    @staticmethod
    def test_points_in_polygon_wkt_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(points_in_polygon_wkt)

    @staticmethod
    def test_points_in_polygon_wkt_unknownPath():
        """ None input raises Value Error. """
        assert_unknown_path_raises_value_error(points_in_polygon_wkt)

    @staticmethod
    def test_points_in_polygon_wkt_nonePath():
        """ If key is None, raise Value Error. """
        assert_none_path_raises_value_error(points_in_polygon_wkt)

    @staticmethod
    def test_points_in_polygon_wkt_Point():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/point.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_Line():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/line.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPoint():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/multipoint.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_MultiLine():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/multiline.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPolygon():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/multipolygon.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_Collection():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/collection.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_invalidPolygon():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/invalid_polygon.wkt")

    @staticmethod
    def test_wkt_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        pc_out = points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/ahn2_polygon.wkt")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        df_out = pd.DataFrame({'x':x, 'y':y})
        df = pd.read_csv("laserchicken/testdata/ahn2_polygon.out", sep=',', header=0, index_col=0, dtype=np.int32)
        assert(pd.DataFrame.equals(df, df_out))

    @staticmethod
    def test_wkt_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        pc_out = points_in_polygon_wkt(pc_in, "laserchicken/testdata/anh2_geometries_wkt/ahn2_polygon_empty.wkt")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)



class TestSpatialSelectionSHP(unittest.TestCase):
    @staticmethod
    def test_points_in_polygon_shp_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(points_in_polygon_shp)

    @staticmethod
    def test_points_in_polygon_shp_unknownPath():
        """ None input raises Value Error. """
        assert_unknown_path_raises_value_error(points_in_polygon_shp)

    @staticmethod
    def test_points_in_polygon_shp_nonePath():
        """ If key is None, raise Value Error. """
        assert_none_path_raises_value_error(points_in_polygon_shp)

    @staticmethod
    def test_points_in_polygon_shp_Point():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/point.shp")

    @staticmethod
    def test_points_in_polygon_shp_Line():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/line.shp")

    @staticmethod
    def test_points_in_polygon_shp_MultiPoint():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/multipoint.shp")

    @staticmethod
    def test_points_in_polygon_shp_MultiLine():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/multiline.shp")

    @staticmethod
    def test_points_in_polygon_shp_MultiPolygon():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/multipolygon.shp")

    @staticmethod
    def test_points_in_polygon_shp_Collection():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/collection.shp")


    @staticmethod
    def test_points_in_polygon_shp_invalidPolygon():
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp(pc_in, "laserchicken/testdata/anh2_geometries_shp/invalid_polygon.shp")

    @staticmethod
    def test_shp_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        pc_out = points_in_polygon_wkt(pc_in, "laserchicken/testdata/ahn2_polygon_shp/ahn2_polygon.shp")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        df_out = pd.DataFrame({'x':x, 'y':y})
        df = pd.read_csv("laserchicken/testdata/ahn2_polygon.out", sep=',', header=0, index_col=0, dtype=np.int32)
        assert(pd.DataFrame.equals(df, df_out))

    @staticmethod
    def test_shp_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        pc_out = points_in_polygon_wkt(pc_in, "laserchicken/testdata/ahn2_polygon_shp/ahn2_polygon_empty.shp")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)

def assert_none_pc_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in, "laserchicken/testdata/ahn2_polygon_shp/ahn2_polygon.wkt")

def assert_unknown_path_raises_value_error(function):
    pc_in = read_las.read("laserchicken/testdata/AHN2.las")
    with pytest.raises(ValueError):
        function(pc_in, 'unknown_path_123')

def assert_none_path_raises_value_error(function):
    pc_in = read_las.read("laserchicken/testdata/AHN2.las")
    with pytest.raises(ValueError):
        function(pc_in, None)