"""Pulse penetration ratio and density absolute mean calculations.

See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/23.
"""

import numpy as np

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class PulsePenetrationFeatureExtractor(AbstractFeatureExtractor):
    """Feature extractor for the point density."""

    # classification according to
    # http://www.asprs.org/wp-content/uploads/2010/12/LAS_1-4_R6.pdf
    ground_tags = [2]

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
        For instance, if a feature extractor returns the first 3 eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        return ['pulse_penetration_ratio', 'density_absolute_mean']

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
        class_neighbors = np.array(point_cloud[point]['raw_classification']["data"][
            neighborhood])

        ground_indices = self._get_ground_indices(
            class_neighbors, self.ground_tags)

        pulse_penetration_ratio = self._get_pulse_penetration_ratio(
            ground_indices, class_neighbors)
        density_absolute_mean = self._get_density_absolute_mean(
            ground_indices, point_cloud)

        return pulse_penetration_ratio, density_absolute_mean

    @staticmethod
    def _get_ground_indices(point_cloud, ground_tags):
        index_grd = []
        for ipt, c in enumerate(point_cloud):
            if c in ground_tags:
                index_grd.append(ipt)
        return index_grd

    @staticmethod
    def _get_pulse_penetration_ratio(ground_indices, class_neighbors):
        n_total = len(class_neighbors)
        n_ground = len(ground_indices)
        return float(n_ground) / n_total

    @staticmethod
    def _get_density_absolute_mean(ground_indices, source_point_cloud):
        n_ground = len(ground_indices)
        z_ground = source_point_cloud[point]['z']["data"][ground_indices]
        if n_ground == 0:
            density_absolute_mean = 0.
        else:
            density_absolute_mean = float(
                len(z_ground[z_ground > np.mean(z_ground)])) / n_ground * 100.
        return density_absolute_mean

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractor object.

        Needed for provenance.
        """
        return ()
