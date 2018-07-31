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
        raise NotImplementedError("Class {} doesn't implement get_type()".format(type(self).__name__))

    def calculate_area_or_volume(self):
        """
        Calculate the area (infinite cylinder. cell) or volume (sphere, cube) depending on the volume type.

        :return: area or volume
        """
        raise NotImplementedError("Class {} doesn't implement calculate_area_or_volume()".format(type(self).__name__))


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

    def calculate_area_or_volume(self):
        return self.calculate_volume()

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

    def calculate_area_or_volume(self):
        return self.calculate_base_area()


class Cell(Volume):
    """Cell that is square in xy plane and extends infinitely to both z and -z direction."""

    TYPE = 'cell'

    def __init__(self, side_length):
        self.side_length = side_length

    def get_type(self):
        return self.TYPE

    def calculate_base_area(self):
        """
        Calculate the area of the base of the cell..

        :return: area of the base
        """
        return np.power(self.side_length, 2)

    def calculate_area_or_volume(self):
        return self.calculate_base_area()


class Cube(Volume):
    """Mathematical cube."""

    TYPE = 'cube'

    def __init__(self, side_length):
        self.side_length = side_length

    def get_type(self):
        return self.TYPE

    def calculate_volume(self):
        """
        Calculate the volume of this sphere based on its radius.

        :return: volume
        """
        return np.power(self.side_length, 3)

    def calculate_area_or_volume(self):
        return self.calculate_volume()
