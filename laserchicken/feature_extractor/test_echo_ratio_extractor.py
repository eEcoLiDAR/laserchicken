import os
import unittest
import random

import pytest
import numpy as np

from laserchicken import keys, load, utils
from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point
from laserchicken.test_tools import create_point_cloud
from laserchicken.volume_specification import Sphere, InfiniteCylinder

from laserchicken.feature_extractor.echo_ratio_feature_extractor import EchoRatioFeatureExtractor


class TestEchoRatioFeatureExtractorArtificialData(unittest.TestCase):
    """Test echo ratio extractor on artificial spherical and cylindric data."""

    point_cloud = None
    target_point_cloud = None

    def test_valid(self):
        """Result must be close to the theoretical value."""

        # extractor = EchoRatioFeatureExtractor()
        extractor = EchoRatioFeatureExtractor()
        per = extractor.extract(
            self.point_cloud, self.neighborhoods, self.target_point_cloud, self.indexpc, self.cylinder)
        np.testing.assert_allclose(per, self.theoretical_value)

    def test_invalid(self):
        """ Must raise TypeError as we do not provide correct indexes."""

        extractor = EchoRatioFeatureExtractor()
        # target point cloud must not be None
        with pytest.raises(ValueError):
            extractor.extract(self.point_cloud, self.neighborhoods, None, self.indexpc, self.cylinder)

        # target index must not be None
        with pytest.raises(ValueError):
            extractor.extract(self.point_cloud, self.neighborhoods, self.target_point_cloud, None, self.cylinder)

        # volume must be a cylinder
        with pytest.raises(ValueError):
            sphere = Sphere(self.radius)
            extractor.extract(self.point_cloud, self.neighborhoods, self.target_point_cloud, self.indexpc, sphere)

    @staticmethod
    def _get_pc(xyz):
        return {keys.point: {'x': {'type': 'double', 'data': xyz[:, 0]},
                             'y': {'type': 'double', 'data': xyz[:, 1]},
                             'z': {'type': 'double', 'data': xyz[:, 2]}}}, len(xyz)

    def _set_sphere_data(self):
        """Create a sphere of point."""
        n_theta, n_phi = 11, 11
        self.npt_sphere = n_theta * n_phi
        theta = np.linspace(0.1, 2 * np.pi, n_theta)
        phi = np.linspace(0.1, np.pi, n_phi)
        r = self.radius
        for t in theta:
            for p in phi:
                x = r * np.cos(t) * np.sin(p)
                y = r * np.sin(t) * np.sin(p)
                z = r * np.cos(p)
                self.xyz.append([x, y, z])

    def _set_cylinder_data(self):
        """Create a cylinder of point."""
        # n_height must be even so that the cylinder has no point
        # on the equator of the sphere
        n_theta, n_height = 11, 10
        self.npt_cyl = n_theta * n_height
        r = self.radius
        theta = np.linspace(0.1, 2 * np.pi, n_theta)
        height = np.linspace(-2 * r, 2 * r, n_height)

        for h in height:
            for t in theta:
                x, y, z = r * np.cos(t), r * np.sin(t), h
                self.xyz.append([x, y, z])

    def _get_central_point(self, index):
        """Get the central point."""
        return utils.copy_point_cloud(self.point_cloud, [index])

    def setUp(self):
        """
        Set up the test.

        Create a sphere and a cylinder of points and a central point
        The cylinder has no points on the equator of the sphere
        """

        # create the points
        self.radius = 0.5
        self.xyz = [[0., 0., 0.]]
        self._set_sphere_data()
        self._set_cylinder_data()

        # create the pc
        self.point_cloud, self.npts = self._get_pc(np.array(self.xyz))
        self.target_point_cloud = self._get_central_point(0)
        self.indexpc = 0

        # create the volume/neighborhood
        self.cylinder = InfiniteCylinder(self.radius + 1E-3)
        self.neighborhoods = list(compute_neighborhoods(self.point_cloud, self.target_point_cloud, self.cylinder))

        # theoretical value of the echo ratio
        self.theoretical_value = (self.npt_sphere + 1) / (self.npt_sphere + self.npt_cyl + 1)


class TestEchoRatioFeatureExtractorSimpleArtificialData(unittest.TestCase):
    """Test echo ratio extractor on artificial spherical and cylindric data."""

    def test_valid(self):
        """Result must be close to the theoretical value."""
        extractor = EchoRatioFeatureExtractor()
        result = extractor.extract(self.environment_pc, self.neighbors, self.target_pc, range(4), self.cylinder)
        np.testing.assert_allclose(result, self.echo_ratios)

    def setUp(self):
        """
        Create a grid of 4 targets and an environment point cloud and neighbors and the echo ratios of those targets.
        """
        self.radius = 0.5
        targets = np.array([[10., 0., 5.], [10., 10., 5.], [0., 0., 5.], [0., 10., 5.]])  # Grid w. steps 10 & height 5
        self.echo_ratios = np.array([0., 0.9, 0.5, 0.8])
        environment_parts = [self._create_environment_part(t, ratio, self.radius) for t, ratio in zip(targets,
                                                                                                      self.echo_ratios)]
        environment = np.vstack(environment_parts)

        self.target_pc = create_point_cloud(targets[:, 0], targets[:, 1], targets[:, 2])
        self.environment_pc = create_point_cloud(environment[:, 0], environment[:, 1], environment[:, 2])

        self.cylinder = InfiniteCylinder(self.radius)
        self.neighbors = list(compute_neighborhoods(self.environment_pc, self.target_pc, self.cylinder))

    @staticmethod
    def _create_environment_part(target, echo_ratio, radius):
        """
        Creates 10 points at the target location, and a given ratio of points outside the radius (above the target)
        :param target:
        :param echo_ratio:
        :param radius:
        :return: numpy array
        """
        ratio = echo_ratio  # Convert from percentage
        n_outside = 10
        n_inside = int(n_outside * ratio / (1 - ratio))
        outside_sphere = np.zeros((n_outside, 3)) + target + np.array([0., 0., 2 * radius])
        inside_sphere = np.zeros((int(n_inside), 3)) + target
        return np.vstack((inside_sphere, outside_sphere))


class EchoRatioFeatureExtractorSequential(FeatureExtractor):
    """Feature extractor for the point density."""

    @classmethod
    def requires(cls):
        """
        Get a list of names of the point attributes that are needed for this feature extraction.
        For simple features, this could be just x, y, and z. Other features can build on again
        other features to have been computed first.
        :return: List of feature names
        """
        return []

    @classmethod
    def provides(cls):
        """
        Get a list of names of the feature values.
        This will return as many names as the number feature values that will be returned.
        For instance, if a feature extractor returns the first 3 Eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.
        :return: List of feature names
        """
        return ['echo_ratio_sequential']

    def extract(self, point_cloud, neighborhood, target_point_cloud, target_index, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.
        :param point_cloud: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_index: index of the target point in the target point cloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature value
        """
        if volume_description.TYPE != 'infinite cylinder':
            raise ValueError('The volume must be a cylinder')

        if target_point_cloud is None:
            raise ValueError('Target point cloud required')

        if target_index is None:
            raise ValueError('Target point index required')

        xyz = self.get_neighborhood_positions(point_cloud, neighborhood)
        n_cylinder = xyz.shape[0]

        xyz0 = self.get_target_position(target_point_cloud, target_index)
        difference = xyz - xyz0
        squared = difference ** 2
        sum_of_squares = np.sum(squared, 1)
        n_sphere = np.sum(sum_of_squares <=
                          volume_description.radius ** 2)
        return n_sphere / n_cylinder

    @staticmethod
    def get_target_position(target_point_cloud, target_index):
        x0 = target_point_cloud[point]['x']['data'][target_index]
        y0 = target_point_cloud[point]['y']['data'][target_index]
        z0 = target_point_cloud[point]['z']['data'][target_index]
        return np.array([x0, y0, z0])

    @staticmethod
    def get_neighborhood_positions(point_cloud, neighborhood):
        x = point_cloud[point]['x']['data'][neighborhood]
        y = point_cloud[point]['y']['data'][neighborhood]
        z = point_cloud[point]['z']['data'][neighborhood]
        return np.column_stack((x, y, z))

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.
        Needed for provenance.
        """
        return ()


if __name__ == '__main__':
    unittest.main()
