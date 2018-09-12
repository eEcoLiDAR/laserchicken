from unittest import TestCase

from numpy.testing import assert_equal, assert_almost_equal

from laserchicken.volume_specification import Sphere, InfiniteCylinder, Cell, Cube


class VolumeTests(TestCase):
    @staticmethod
    def test_sphere_correctType():
        assert_equal(Sphere(1).get_type(), Sphere.TYPE)

    @staticmethod
    def test_sphere_calculateVolume():
        assert_almost_equal(Sphere(2).calculate_volume(), 33.510321638)

    @staticmethod
    def test_infiniteCylinder_type():
        assert_equal(InfiniteCylinder(2).get_type(), InfiniteCylinder.TYPE)

    @staticmethod
    def test_infiniteCylinder_calculateArea():
        assert_almost_equal(InfiniteCylinder(2).calculate_base_area(), 12.56637061436)

    @staticmethod
    def test_cell_type():
        assert_equal(Cell(2).get_type(), Cell.TYPE)

    @staticmethod
    def test_cell_calculateArea():
        assert_almost_equal(Cell(2).calculate_base_area(), 4.0)

    @staticmethod
    def test_cube_correctType():
        assert_equal(Cube(1).get_type(), Cube.TYPE)

    @staticmethod
    def test_cube_calculateVolume():
        assert_almost_equal(Cube(2).calculate_volume(), 8.0)
