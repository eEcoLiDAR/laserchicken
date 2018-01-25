import unittest
import pytest

from laserchicken import read_las
from laserchicken.density import area_density, area_density_rad, volume_density, volume_density_rad

class TestAreaDensity(unittest.TestCase):
    @staticmethod
    def test_area_density_pc_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(area_density)

    @staticmethod
    def test_area_density_pc_None_Rad():
        """ None input raises Value Error. """
        assert_none_pc_rad_raises_value_error(area_density_rad)

    @staticmethod
    def test_area_density_pc_rad_None():
        """ None input raises Value Error. """
        assert_pc_none_rad_raises_value_error(area_density)

    @staticmethod
    def test_area_density_pc_rad_Neg():
        """ None input raises Value Error. """
        assert_pc_neg_rad_raises_value_error(area_density_rad)

    @staticmethod
    def test_area_density_pc_rad_Zero():
        """ None input raises Value Error. """
        assert_pc_zero_rad_raises_value_error(area_density_rad)

    @staticmethod
    def test_area_density_pc():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        density = area_density(pc_in)
        assert(density == 6.868558718435157)

    @staticmethod
    def test_area_density_pc_rad():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        density = area_density_rad(pc_in, 75)
        assert (density == 1212)

class TestVolumneDensity(unittest.TestCase):
    @staticmethod
    def test_volume_density_pc_None():
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(volume_density)

    @staticmethod
    def test_volume_density_pc_None_Rad():
        """ None input raises Value Error. """
        assert_none_pc_rad_raises_value_error(volume_density)

    @staticmethod
    def test_volume_density_pc_rad_None():
        """ None input raises Value Error. """
        assert_pc_none_rad_raises_value_error(volume_density_rad)

    @staticmethod
    def test_volume_density_pc_rad_Neg():
        """ None input raises Value Error. """
        assert_pc_neg_rad_raises_value_error(volume_density_rad)

    @staticmethod
    def test_volume_density_pc_rad_Zero():
        """ None input raises Value Error. """
        assert_pc_zero_rad_raises_value_error(volume_density_rad)

    @staticmethod
    def test_volume_density_pc():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        density = volume_density(pc_in)
        assert(density == 6.868558718435157)

    @staticmethod
    def test_volume_density_pc_rad():
        """ Selecting all points within a Polygon. """
        pc_in = read_las.read("testdata/AHN2.las")
        density = volume_density_rad(pc_in, 75)
        assert (density == 1212)


def assert_none_pc_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in)

def assert_none_pc_rad_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in, 1.0)

def assert_pc_none_rad_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = read_las.read("testdata/AHN2.las")
        function(pc_in, None)

def assert_pc_neg_rad_raises_value_error(function):
    pc_in = read_las.read("testdata/AHN2.las")
    with pytest.raises(ValueError):
        function(pc_in, -1)

def assert_pc_zero_rad_raises_value_error(function):
    pc_in = read_las.read("testdata/AHN2.las")
    with pytest.raises(ValueError):
        function(pc_in, 0)