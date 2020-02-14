"""Calculate echo ratio.

See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/21
"""

import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.utils import get_attributes_per_neighborhood


def _to_unmasked_array(masked_array):
    """Creates a 'normal' numpy array from a masked array, inputting nans for masked values."""
    data = masked_array.data
    data[masked_array.mask] = np.nan
    return data


class BandRatioFeatureExtractor(FeatureExtractor):
    """Feature extractor for the point density."""

    def __init__(self, lower_limit, upper_limit, data_key='z'):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.data_key = data_key

    def requires(self):
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
        For instance, if a feature extractor returns the first 3 Eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        name = 'band_ratio_'
        if self.lower_limit is not None:
            name += str(self.lower_limit) + '<'
        name += self.data_key
        if self.upper_limit is not None:
            name += '<' + str(self.upper_limit)
        return [name]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_index, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param point_cloud: environment (search space) point cloud
        :param neighborhoods: array of array of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_index: index of the target point in the target point cloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature value
        """
        supported_volumes = ['infinite cylinder', 'cell']
        if volume_description.TYPE not in supported_volumes:
            raise ValueError('The volume must be a cylinder')

        attribute = get_attributes_per_neighborhood(point_cloud, neighborhoods, [self.data_key])
        z = attribute[:, 0, :]
        n_total_points = attribute.shape[2]
        n_masked_points_per_neighborhood = attribute.mask[:, 0, :].sum(axis=1)
        n_points_per_neighborhood = -n_masked_points_per_neighborhood + n_total_points
        is_point_below_upper_limit = z < self.upper_limit if self.upper_limit else np.ones_like(z)
        is_point_above_lower_limit = z > self.lower_limit if self.lower_limit else np.ones_like(z)
        n_points_within_band = np.sum(is_point_below_upper_limit * is_point_above_lower_limit, axis=1)
        return _to_unmasked_array(n_points_within_band / n_points_per_neighborhood)

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractor object.

        Needed for provenance.
        """
        return (self.lower_limit, self.upper_limit, self.data_key)
