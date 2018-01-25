import unittest

import numpy as np
import pytest
from numpy.testing import assert_equal, assert_almost_equal

from laserchicken.keys import point
from laserchicken.select import select_below, select_above, select_equal


class TestSelectEqual(unittest.TestCase):
    @staticmethod
    def test_selectEqual_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_equal)

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
    def test_selectEqual_outputEmpty():
        """ Correct number of results. """
        pc_in = get_test_data()
        pc_out = select_equal(pc_in, 'return', 1)
        assert_equal(len(pc_out[point]['x']['data']), 2)


class TestSelectBelow(unittest.TestCase):
    @staticmethod
    def test_selectBelow_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_below)

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
        assert_none_pc_raises_value_error(select_above)

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


def assert_none_pc_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in, 'x', 13)


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
