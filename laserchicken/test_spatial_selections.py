import os
import shutil
import unittest
import pytest

import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal, assert_equal

from laserchicken.keys import point
from laserchicken import read_las
from laserchicken.spatial_selections import points_in_polygon_wkt, points_in_polygon_wkt_file, \
    points_in_polygon_shp_file
from laserchicken.test_tools import ComplexTestData


class TestSpatialSelectionWKT(unittest.TestCase):
    polygon_around_1_point_ahn2 = "POLYGON(( 243627.840248 572073.439002, 243627.842248 572073.439002, 243627.842248 572073.441002, 243627.840248 572073.441002, 243627.840248 572073.439002))"

    @staticmethod
    def test_points_in_polygon_wkt_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(points_in_polygon_wkt)

    @staticmethod
    def test_points_in_polygon_wkt_noneWKT():
        """ If key is None, raise Value Error. """
        assert_none_wkt_raises_value_error(points_in_polygon_wkt)

    @staticmethod
    def test_points_in_polygon_wkt_Point():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "POINT(6 10)")

    @staticmethod
    def test_points_in_polygon_wkt_Line():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "LINESTRING(3 4,10 50,20 25)")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPoint():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "MULTIPOINT(3.5 5.6, 4.8 10.5)")

    @staticmethod
    def test_points_in_polygon_wkt_MultiLine():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "MULTILINESTRING((3 4,10 50,20 25),(-5 -8,-10 -8,-15 -4))")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPolygon():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in,
                                  "MULTIPOLYGON(((1 1,5 1,5 5,1 5,1 1),(2 2, 3 2, 3 3, 2 3,2 2)),((3 3,6 2,6 4,3 3)))")

    @staticmethod
    def test_points_in_polygon_wkt_Collection():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in, "GEOMETRYCOLLECTION(POINT(4 6),LINESTRING(4 6,7 10))")

    @staticmethod
    def test_points_in_polygon_wkt_invalidPolygon():
        """Polygon is not closed so should raise error."""
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt(pc_in,
                                  "POLYGON(( 243590.0 572110.0, 243640.0 572160.0, 243700.0 572110.0, 243640.0 572060.0 ))")

    @staticmethod
    def test_wkt_polygons_contains():
        """ Selecting all points within a Polygon using artificial data. """
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        expected_point = np.array(pc_in[point]['x']['data'][0], pc_in[point]['y']['data'][0])
        pc_out = points_in_polygon_wkt(pc_in, test_data.get_wkt_polygon_around_first_point_only())
        assert_equal(len(pc_out[point]['x']['data']), 1)
        selected_point = np.array(pc_out[point]['x']['data'][0], pc_out[point]['y']['data'][0])
        np.testing.assert_allclose(selected_point, expected_point)

    def test_wkt_polygons_contains_single_point(self):
        """Selecting a single point with a tiny polygon. Test for https://github.com/eEcoLiDAR/eEcoLiDAR/issues/64. """
        pc_in = read_las.read("testdata/AHN2.las")
        pc_out = points_in_polygon_wkt(pc_in, self.polygon_around_1_point_ahn2)
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        expected_x = 243627.841248
        expected_y = 572073.440002
        assert_equal(len(x), 1)
        assert_almost_equal(x[0], expected_x, 4)
        assert_almost_equal(y[0], expected_y, 4)

    def test_wkt_polygons_contains_original_not_changed(self):
        """Point cloud in should not change by filtering."""
        pc_in = read_las.read("testdata/AHN2.las")
        len_x_before = len(pc_in[point]['x']['data'])
        _pc_out = points_in_polygon_wkt(pc_in, self.polygon_around_1_point_ahn2)
        len_x_after = len(pc_in[point]['x']['data'])
        assert_equal(len_x_after, len_x_before)

    @staticmethod
    def test_wkt_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        pc_out = points_in_polygon_wkt(pc_in,
                                       "POLYGON(( 253590.0 582110.0, 253640.0 582160.0, 253700.0 582110.0, 253640.0 582060.0, 253590.0 582110.0 ))")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)


class TestSpatialSelectionWKTFile(unittest.TestCase):
    _test_dir = 'wkt_test_dir'

    @staticmethod
    def test_points_in_polygon_wkt_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(points_in_polygon_wkt_file)

    @staticmethod
    def test_points_in_polygon_wkt_unknownPath():
        """ None input raises Value Error. """
        assert_unknown_path_raises_value_error(points_in_polygon_wkt_file)

    @staticmethod
    def test_points_in_polygon_wkt_nonePath():
        """ If key is None, raise Value Error. """
        assert_none_path_raises_value_error(points_in_polygon_wkt_file)

    @staticmethod
    def test_points_in_polygon_wkt_Point():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/point.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_Line():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/line.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPoint():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/multipoint.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_MultiLine():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/multiline.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPolygon():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/multipolygon.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_Collection():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/collection.wkt")

    @staticmethod
    def test_points_in_polygon_wkt_invalidPolygon():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/invalid_polygon.wkt")

    def test_wkt_polygons_contains(self):
        """Selecting all points within a Polygon with artificial data."""
        test_data = ComplexTestData()
        path = os.path.join(self._test_dir, 'wkt_test.wkt')
        with open(path, 'w') as f:
            f.write(test_data.get_wkt_polygon_around_first_point_only())
        pc_in = test_data.get_point_cloud()
        expected_point = np.array(pc_in[point]['x']['data'][0], pc_in[point]['y']['data'][0])

        pc_out = points_in_polygon_wkt_file(pc_in, path)

        assert_equal(len(pc_out[point]['x']['data']), 1)
        selected_point = np.array(pc_out[point]['x']['data'][0], pc_out[point]['y']['data'][0])
        np.testing.assert_allclose(selected_point, expected_point)

    @staticmethod
    def test_wkt_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        pc_out = points_in_polygon_wkt_file(pc_in, "testdata/ahn2_geometries_wkt/ahn2_polygon_empty.wkt")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)

class TestSpatialSelectionSHPFile(unittest.TestCase):
    @staticmethod
    def test_points_in_polygon_shp_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(points_in_polygon_shp_file)

    @staticmethod
    def test_points_in_polygon_shp_unknownPath():
        """ None input raises Value Error. """
        assert_unknown_path_raises_value_error(points_in_polygon_shp_file)

    @staticmethod
    def test_points_in_polygon_shp_nonePath():
        """ If key is None, raise Value Error. """
        assert_none_path_raises_value_error(points_in_polygon_shp_file)

    @staticmethod
    def test_points_in_polygon_shp_Point():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/point.shp")

    @staticmethod
    def test_points_in_polygon_shp_Line():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/line.shp")

    @staticmethod
    def test_points_in_polygon_shp_MultiPoint():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/multipoint.shp")

    @staticmethod
    def test_points_in_polygon_shp_MultiLine():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/multiline.shp")

    @staticmethod
    def test_points_in_polygon_shp_Collection():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/collection.shp")

    @staticmethod
    def test_points_in_polygon_shp_invalidPolygon():
        pc_in = read_las.read("testdata/AHN2.las")
        with pytest.raises(ValueError):
            points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/invalid_polygon.shp")

    @staticmethod
    def test_shp_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        pc_out = points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/ahn2_polygon.shp")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        # Seemingly redundant 'astype' call: since pandas 0.24 Dataframe() doesn't enforce the given dtype as before
        df_out = pd.DataFrame({'x': x, 'y': y}, dtype=np.int32).astype(dtype=np.int32)
        df = pd.read_csv("testdata/ahn2_polygon.out", sep=',', header=0, index_col=0, dtype=np.int32)
        assert (pd.DataFrame.equals(df, df_out))

    @staticmethod
    def test_shp_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        pc_out = points_in_polygon_shp_file(pc_in, "testdata/ahn2_geometries_shp/ahn2_polygon_empty.shp")
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)


def assert_none_pc_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in, "testdata/ahn2_polygon_shp/ahn2_polygon.wkt")


def assert_unknown_path_raises_value_error(function):
    pc_in = read_las.read("testdata/AHN2.las")
    with pytest.raises(Exception):
        function(pc_in, 'unknown_path_123')


def assert_none_path_raises_value_error(function):
    pc_in = read_las.read("testdata/AHN2.las")
    with pytest.raises(Exception):
        function(pc_in, None)


def assert_none_wkt_raises_value_error(function):
    pc_in = read_las.read("testdata/AHN2.las")
    with pytest.raises(ValueError):
        function(pc_in, None)
