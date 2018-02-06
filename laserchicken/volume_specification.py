"""Classes that describe volumes."""
import numpy as np

SPHERE_VOLUME_FACTOR = 4 * np.pi / 3


class Volume(object):
    """Abstract class for volume descriptions."""

    def get_type(self):
        """
        Give the type as a string like 'sphere' or 'cylinder'.

        :return: type description
        """
        raise NotImplementedError("Class {} doesn't implement get_requirements()".format(type(self).__name__))


class Sphere(Volume):
    """Mathematical sphere."""

    TYPE = 'sphere'

    def __init__(self, radius):
        self.radius = radius

    def get_type(self):
        return self.TYPE

    def calculate_volume(self):
        """
        Calculate the volume of this sphere based on its radius.

        :return: volume
        """
        return np.power(self.radius, 3) * SPHERE_VOLUME_FACTOR


class InfiniteCylinder(Volume):
    """Cylinder with base in the xy plane and height that extends infinitely to both z and -z direction."""

    TYPE = 'infinite cylinder'

    def __init__(self, radius):
        self.radius = radius

    def get_type(self):
        return self.TYPE

    def calculate_base_area(self):
        """
        Calculate the area of the base of the infinite cylinder.

        :return: area of the base
        """
        return np.power(self.radius, 2) * np.pi
