import os
import shutil
import unittest

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_equal, assert_almost_equal

from laserchicken import load
from laserchicken.keys import point
from laserchicken.filter import select_below, select_above, select_equal, select_polygon
from laserchicken.test_tools import ComplexTestData


class TestSelectEqual(unittest.TestCase):
    @staticmethod
    def test_selectEqual_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_equal, 'x', 13)

    @staticmethod
    def test_selectEqual_unknownKey():
        """ If key is not in point cloud, raise Value Error. """
        assert_unknown_key_raises_value_error(select_equal)

    @staticmethod
    def test_selectEqual_noneKey():
        """ If key is None, raise Value Error. """
        assert_none_key_raises_value_error(select_equal)

    @staticmethod
    def test_selectEqual_outputIsNotInput():
        """ Select change output, make sure that input hasn't changed. """
        assert_output_is_not_input(select_equal)

    @staticmethod
    def test_selectEqual_outputEmpty():
        """ Select everything equal to something that doesn't exist should result in empty output. """
        pc_in = get_test_data()
        pc_out = select_equal(pc_in, 'return', 5)
        assert_equal(len(pc_out[point]['x']['data']), 0)

    @staticmethod
    def test_selectEqual_outputCorrect():
        """ Correct number of results. """
        pc_in = get_test_data()
        pc_out = select_equal(pc_in, 'return', 1)
        assert_equal(len(pc_out[point]['x']['data']), 2)


class TestSelectBelow(unittest.TestCase):
    @staticmethod
    def test_selectBelow_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_below, 'x', 13)

    @staticmethod
    def test_selectBelow_unknownKey():
        """ If key is not in point cloud, raise Value Error. """
        assert_unknown_key_raises_value_error(select_below)

    @staticmethod
    def test_selectBelow_noneKey():
        """ If key is None, raise Value Error. """
        assert_none_key_raises_value_error(select_below)

    @staticmethod
    def test_selectBelow_outputIsNotInput():
        """ Select change output, make sure that input hasn't changed. """
        assert_output_is_not_input(select_below)

    @staticmethod
    def test_selectBelow_everything():
        """ Selecting all point under some super high value should return all the points. """
        pc_in = get_test_data()
        pc_out = select_below_ridiculous_high_z(pc_in)
        assert_equal(len(pc_out[point]['x']['data']), 3)
        assert_points_equal(pc_in, pc_out)

    @staticmethod
    def test_selectBelow_onlyOnePoint():
        """ Selecting below some threshold should only result the correct lowest point. """
        pc_in = get_test_data()
        pc_out = select_below(pc_in, 'z', 3.2)
        assert_equal(len(pc_out[point]['x']['data']), 1)
        assert_almost_equal(pc_out[point]['x']['data'][0], 1.1)
        assert_almost_equal(pc_out[point]['y']['data'][0], 2.1)
        assert_almost_equal(pc_out[point]['z']['data'][0], 3.1)
        assert_almost_equal(pc_out[point]['return']['data'][0], 1)


class TestSelectAbove(unittest.TestCase):
    @staticmethod
    def test_selectAbove_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_above, 'x', 13)

    @staticmethod
    def test_selectAbove_unknownKey():
        """ If key is not in point cloud, raise Value Error. """
        assert_unknown_key_raises_value_error(select_above)

    @staticmethod
    def test_selectAbove_noneKey():
        """ If key is None, raise Value Error. """
        assert_none_key_raises_value_error(select_above)

    @staticmethod
    def test_selectAbove_outputIsNotInput():
        """ Select change output, make sure that input hasn't changed. """
        assert_output_is_not_input(select_above)

    @staticmethod
    def test_selectAbove_everything():
        """ Selecting all point above some super low value should return all the points. """
        pc_in = get_test_data()
        pc_out = select_above(pc_in, 'z', -100000)
        assert_points_equal(pc_in, pc_out)

    @staticmethod
    def test_selectBelow_onlyOnePoint():
        """ Selecting above some threshold should only result the correct highest point. """
        pc_in = get_test_data()
        pc_out = select_above(pc_in, 'z', 3.2)
        assert_equal(len(pc_out[point]['x']['data']), 1)
        assert_almost_equal(pc_out[point]['x']['data'][0], 1.3)
        assert_almost_equal(pc_out[point]['y']['data'][0], 2.3)
        assert_almost_equal(pc_out[point]['z']['data'][0], 3.3)
        assert_almost_equal(pc_out[point]['return']['data'][0], 2)


class TestSelectPolygonWKT(unittest.TestCase):
    polygon_around_1_point_ahn2 = ("POLYGON(( 243627.840248 572073.439002, "
                                   "243627.842248 572073.439002, "
                                   "243627.842248 572073.441002, "
                                   "243627.840248 572073.441002, "
                                   "243627.840248 572073.439002))")

    @staticmethod
    def test_points_in_polygon_wkt_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_polygon, "POLYGON((0.,0.,0.))")

    @staticmethod
    def test_points_in_polygon_wkt_noneWKT():
        """ If key is None, raise Value Error. """
        assert_none_wkt_raises_value_error(select_polygon)

    @staticmethod
    def test_points_in_polygon_wkt_Point():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "POINT(6 10)")

    @staticmethod
    def test_points_in_polygon_wkt_Line():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "LINESTRING(3 4,10 50,20 25)")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPoint():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "MULTIPOINT(3.5 5.6, 4.8 10.5)")

    @staticmethod
    def test_points_in_polygon_wkt_MultiLine():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "MULTILINESTRING((3 4,10 50,20 25),(-5 -8,-10 -8,-15 -4))")

    @staticmethod
    def test_points_in_polygon_wkt_MultiPolygon():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in,
                           "MULTIPOLYGON(((1 1,5 1,5 5,1 5,1 1),(2 2, 3 2, 3 3, 2 3,2 2)),((3 3,6 2,6 4,3 3)))")

    @staticmethod
    def test_points_in_polygon_wkt_Collection():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "GEOMETRYCOLLECTION(POINT(4 6),LINESTRING(4 6,7 10))")

    @staticmethod
    def test_points_in_polygon_wkt_invalidPolygon():
        """Polygon is not closed so should raise error."""
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in,
                           "POLYGON(( 243590.0 572110.0, 243640.0 572160.0, 243700.0 572110.0, 243640.0 572060.0 ))")

    @staticmethod
    def test_wkt_polygons_contains():
        """ Selecting all points within a Polygon using artificial data. """
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        expected_point = np.array(pc_in[point]['x']['data'][0], pc_in[point]['y']['data'][0])
        pc_out = select_polygon(pc_in, test_data.get_wkt_polygon_around_first_point_only())
        assert_equal(len(pc_out[point]['x']['data']), 1)
        selected_point = np.array(pc_out[point]['x']['data'][0], pc_out[point]['y']['data'][0])
        np.testing.assert_allclose(selected_point, expected_point)

    def test_wkt_polygons_contains_single_point(self):
        """Selecting a single point with a tiny polygon. Test for https://github.com/eEcoLiDAR/eEcoLiDAR/issues/64. """
        pc_in = load("testdata/AHN2.las")
        pc_out = select_polygon(pc_in, self.polygon_around_1_point_ahn2)
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        expected_x = 243627.841248
        expected_y = 572073.440002
        assert_equal(len(x), 1)
        assert_almost_equal(x[0], expected_x, 4)
        assert_almost_equal(y[0], expected_y, 4)

    def test_wkt_polygons_contains_original_not_changed(self):
        """Point cloud in should not change by filtering."""
        pc_in = load("testdata/AHN2.las")
        len_x_before = len(pc_in[point]['x']['data'])
        _pc_out = select_polygon(pc_in, self.polygon_around_1_point_ahn2)
        len_x_after = len(pc_in[point]['x']['data'])
        assert_equal(len_x_after, len_x_before)

    @staticmethod
    def test_wkt_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = load("testdata/AHN2.las")
        pc_out = select_polygon(pc_in,
                                ("POLYGON(( 253590.0 582110.0, "
                                 "253640.0 582160.0, 253700.0 582110.0, "
                                 "253640.0 582060.0, 253590.0 582110.0 ))"))
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)


class TestSelectPolygonWKTFile(unittest.TestCase):
    _test_dir = 'wkt_test_dir'

    @staticmethod
    def test_points_in_polygon_wkt_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_polygon,
                                          "testdata/ahn2_polygon_shp/ahn2_polygon.wkt",
                                          read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_unknownPath():
        """ None input raises Value Error. """
        assert_unknown_path_raises_value_error(select_polygon)

    @staticmethod
    def test_points_in_polygon_wkt_nonePath():
        """ If key is None, raise Value Error. """
        assert_none_path_raises_value_error(select_polygon)

    @staticmethod
    def test_points_in_polygon_wkt_Point():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/point.wkt", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_Line():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/line.wkt", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_MultiPoint():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/multipoint.wkt", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_MultiLine():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/multiline.wkt", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_MultiPolygon():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/multipolygon.wkt", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_Collection():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/collection.wkt", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_wkt_invalidPolygon():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_wkt/invalid_polygon.wkt", read_from_file=True)

    def test_wkt_polygons_contains(self):
        """Selecting all points within a Polygon with artificial data."""
        test_data = ComplexTestData()
        path = os.path.join(self._test_dir, 'wkt_test.wkt')
        with open(path, 'w') as f:
            f.write(test_data.get_wkt_polygon_around_first_point_only())
        pc_in = test_data.get_point_cloud()
        expected_point = np.array(pc_in[point]['x']['data'][0], pc_in[point]['y']['data'][0])

        pc_out = select_polygon(pc_in, path, read_from_file=True)

        assert_equal(len(pc_out[point]['x']['data']), 1)
        selected_point = np.array(pc_out[point]['x']['data'][0], pc_out[point]['y']['data'][0])
        np.testing.assert_allclose(selected_point, expected_point)

    @staticmethod
    def test_wkt_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = load("testdata/AHN2.las")
        pc_out = select_polygon(pc_in, "testdata/ahn2_geometries_wkt/ahn2_polygon_empty.wkt", read_from_file=True)
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)


class TestSelectPolygonSHPFile(unittest.TestCase):
    @staticmethod
    def test_points_in_polygon_shp_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_polygon,
                                          "testdata/ahn2_geometries_shp/point.shp",
                                          read_from_file=True)

    @staticmethod
    def test_points_in_polygon_shp_unknownPath():
        """ None input raises Value Error. """
        assert_unknown_path_raises_value_error(select_polygon)

    @staticmethod
    def test_points_in_polygon_shp_nonePath():
        """ If key is None, raise Value Error. """
        assert_none_path_raises_value_error(select_polygon)

    @staticmethod
    def test_points_in_polygon_shp_Point():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_shp/point.shp", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_shp_Line():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_shp/line.shp", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_shp_MultiPoint():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_shp/multipoint.shp", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_shp_MultiLine():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_shp/multiline.shp", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_shp_Collection():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_shp/collection.shp", read_from_file=True)

    @staticmethod
    def test_points_in_polygon_shp_invalidPolygon():
        pc_in = load("testdata/AHN2.las")
        with pytest.raises(ValueError):
            select_polygon(pc_in, "testdata/ahn2_geometries_shp/invalid_polygon.shp", read_from_file=True)

    @staticmethod
    def test_shp_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = load("testdata/AHN2.las")
        pc_out = select_polygon(pc_in, "testdata/ahn2_geometries_shp/ahn2_polygon.shp", read_from_file=True)
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        # Seemingly redundant 'astype' call: since pandas 0.24 Dataframe() doesn't enforce the given dtype as before
        df_out = pd.DataFrame({'x': x, 'y': y}, dtype=np.int32).astype(dtype=np.int32)
        df = pd.read_csv("testdata/ahn2_polygon.out", sep=',', header=0, index_col=0, dtype=np.int32)
        assert (pd.DataFrame.equals(df, df_out))

    @staticmethod
    def test_shp_polygons_containsEmpty():
        """ Selecting all points within a Polygon. """
        pc_in = load("testdata/AHN2.las")
        pc_out = select_polygon(pc_in, "testdata/ahn2_geometries_shp/ahn2_polygon_empty.shp", read_from_file=True)
        x = pc_out[point]['x']['data']
        y = pc_out[point]['y']['data']
        assert (len(x) == 0)
        assert (len(y) == 0)


def get_test_data():
    return {'log': ['Processed by module load', 'Processed by module filter using parameters(x,y,z)'],
            'pointcloud': {'offset': {'type': 'float', 'data': 12.1}},
            point:
                {'x': {'type': 'float', 'data': np.array([1.1, 1.2, 1.3])},
                 'y': {'type': 'float', 'data': np.array([2.1, 2.2, 2.3])},
                 'z': {'type': 'float', 'data': np.array([3.1, 3.2, 3.3])},
                 'return': {'type': 'int', 'data': np.array([1, 1, 2])}}}


def select_below_ridiculous_high_z(pc_in):
    return select_below(pc_in, 'z', 100000)


def assert_points_equal(pc_in, pc_out):
    assert_equal(len(pc_out[point]['x']['data']), len(pc_in[point]['x']['data']))
    assert_almost_equal(pc_out[point]['x']['data'], pc_in[point]['x']['data'])
    assert_almost_equal(pc_out[point]['y']['data'], pc_in[point]['y']['data'])
    assert_almost_equal(pc_out[point]['z']['data'], pc_in[point]['z']['data'])
    assert_almost_equal(pc_out[point]['return']['data'], pc_in[point]['return']['data'])


def assert_none_pc_raises_value_error(function, *args, **kwargs):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in, *args, **kwargs)


def assert_unknown_key_raises_value_error(function):
    pc = get_test_data()
    with pytest.raises(ValueError):
        function(pc, 'unknown_key_123', 13)


def assert_none_key_raises_value_error(function):
    pc = get_test_data()
    with pytest.raises(ValueError):
        function(pc, None, 13)


def assert_output_is_not_input(function):
    pc_in = get_test_data()
    pc_out = function(pc_in, 'z', 3.2)
    pc_out[point]['x']['data'][0] += 1
    assert_points_equal(pc_in, get_test_data())


def assert_unknown_path_raises_value_error(function):
    pc_in = load("testdata/AHN2.las")
    with pytest.raises(Exception):
        function(pc_in, 'unknown_path_123', read_from_file=True)


def assert_none_path_raises_value_error(function):
    pc_in = load("testdata/AHN2.las")
    with pytest.raises(Exception):
        function(pc_in, None, read_from_file=True)


def assert_none_wkt_raises_value_error(function):
    pc_in = load("testdata/AHN2.las")
    with pytest.raises(ValueError):
        function(pc_in, None)
