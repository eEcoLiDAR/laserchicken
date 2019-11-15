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


class DensityAbsoluteMeanFeatureExtractor(FeatureExtractor):
    """Feature extractor for the point density."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        """
        Get a list of names of the point attributes that are needed for this feature extraction.

        For simple features, this could be just x, y, and z. Other features can build on again
        other features to have been computed first.

        :return: List of feature names
        """
        return []

    def provides(self):
        """
        Get a list of names of the feature values.

        This will return as many names as the number feature values that will be returned.
        For instance, if a feature extractor returns the first 3 eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        return ['density_absolute_mean_' + self.data_key]

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
        if 'raw_classification' not in point_cloud[point]:
            raise ValueError(
                'Missing raw_classification attribute which is necessary for calculating density_absolute_mean.')

        non_ground_indices = [i for i in neighborhood if not _is_ground(i, point_cloud)]
        density_absolute_mean_z = self._get_density_absolute_mean(non_ground_indices, point_cloud)

        return density_absolute_mean_z

    @staticmethod
    def _get_ground_indices(point_cloud, ground_tags):
        index_grd = []
        for ipt, c in enumerate(point_cloud):
            if c in ground_tags:
                index_grd.append(ipt)
        return index_grd

    def _get_density_absolute_mean(self, non_ground_indices, source_point_cloud):
        n_non_ground = len(non_ground_indices)
        data_non_ground = source_point_cloud[point][self.data_key]["data"][non_ground_indices]
        if n_non_ground == 0:
            density_absolute_mean = 0.
        else:
            density_absolute_mean = float(
                len(data_non_ground[data_non_ground > np.mean(data_non_ground)])) / n_non_ground * 100.
        return density_absolute_mean

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractor object.

        Needed for provenance.
        """
        return ()
