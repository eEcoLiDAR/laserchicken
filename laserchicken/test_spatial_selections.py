import unittest

from laserchicken.keys import point
from laserchicken import read_las
from laserchicken.spatial_selections import points_in_polygon_wkt, points_in_polygon_shp

class TestSpatialSelection(unittest.TestCase):
    @staticmethod
    def test_wkt_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        x = pc_in[point]['x']['data']
        y = pc_in[point]['y']['data']
        pc_out = points_in_polygon_wkt(pc_in, "laserchicken/testdata/ahn2_polygon.wkt")
        print (x.size, y.size, pc_out[point]['x']['data'].size, pc_out[point]['y']['data'].size)

    @staticmethod
    def test_shp_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("laserchicken/testdata/AHN2.las")
        x = pc_in[point]['x']['data']
        y = pc_in[point]['y']['data']
        pc_out = points_in_polygon_shp(pc_in, "laserchicken/testdata/ahn2_polygon_shp/ahn2_polygon.shx")
        print (x.size, y.size, pc_out[point]['x']['data'].size, pc_out[point]['y']['data'].size)

    test_shp_polygons_contains()
