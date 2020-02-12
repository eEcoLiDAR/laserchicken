"""Pulse penetration ratio and density absolute mean calculations.

See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/23.
"""

import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point, normalized_height

# classification according to
# http://www.asprs.org/wp-content/uploads/2010/12/LAS_1-4_R6.pdf
GROUND_TAGS = [2]


def _is_ground(i, point_cloud):
    return point_cloud[point]['raw_classification']["data"][i] in GROUND_TAGS


class PulsePenetrationFeatureExtractor(FeatureExtractor):
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
        For instance, if a feature extractor returns the first 3 eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        return ['pulse_penetration_ratio']

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param point_cloud: environment (search space) point cloud
        :param neighborhoods: list of arrays of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_indices: list of indices of the target point in the target point cloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature values
        """
        return [self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]

    def _extract_one(self, point_cloud, neighborhood):
        if 'raw_classification' not in point_cloud[point]:
            raise ValueError(
                'Missing raw_classification attribute which is necessary for calculating pulse_penetratio and '
                'density_absolute_mean features.')

        ground_indices = [i for i in neighborhood if _is_ground(i, point_cloud)]
        pulse_penetration_ratio = self._get_pulse_penetration_ratio(
            ground_indices, len(neighborhood))

        return pulse_penetration_ratio

    @staticmethod
    def _get_ground_indices(point_cloud, ground_tags):
        index_grd = []
        for ipt, c in enumerate(point_cloud):
            if c in ground_tags:
                index_grd.append(ipt)
        return index_grd

    @staticmethod
    def _get_pulse_penetration_ratio(ground_indices, n_total_points):
        n_total = max(n_total_points, 1)
        n_ground = len(ground_indices)
        return float(n_ground) / n_total

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractor object.

        Needed for provenance.
        """
        return ()
