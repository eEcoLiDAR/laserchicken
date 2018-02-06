from unittest import TestCase

from numpy.testing import assert_equal, assert_almost_equal

from laserchicken.volume_specification import Sphere, InfiniteCylinder


class VolumeTests(TestCase):
    @staticmethod
    def test_sphere_correctType():
        assert_equal(Sphere(1).get_type(), Sphere._type_description)

    @staticmethod
    def test_sphere_calculateVolume():
        assert_almost_equal(Sphere(2).calculate_volume(), 33.510321638)

    @staticmethod
    def test_infiniteCylinder_type():
        assert_equal(InfiniteCylinder(2).get_type(), InfiniteCylinder._type_description)

    @staticmethod
    def test_infiniteCylinder_calculateArea():
        assert_almost_equal(InfiniteCylinder(2).calculate_base_area(), 12.56637061436)
