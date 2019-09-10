"""Calculate echo ratio.

See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/21
"""

import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point
from laserchicken.utils import get_xyz, get_point


class BandRatioFeatureExtractor(FeatureExtractor):
    """Feature extractor for the point density."""
    is_vectorized = True

    def __init__(self, lower_limit, upper_limit):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    @classmethod
    def requires(cls):
        """
        Get a list of names of the point attributes that are needed for this feature extraction.

        For simple features, this could be just x, y, and z. Other features can build on again
        other features to have been computed first.

        :return: List of feature names
        """
        return ['band_ratio_{}-{}'.format()]

    @classmethod
    def provides(cls):
        """
        Get a list of names of the feature values.

        This will return as many names as the number feature values that will be returned.
        For instance, if a feature extractor returns the first 3 Eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        return ['band_ratio']

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_index, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param point_cloud: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_index: index of the target point in the target point cloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature value
        """
        if volume_description.TYPE is not 'infinite cylinder' and volume_description.TYPE is not 'cell':
            raise ValueError('The volume must be a cylinder')

        xyz = get_xyz(point_cloud, neighborhoods)
        z = xyz[:, 2, :]
        return np.sum((z < self.upper_limit) * (z > self.lower_limit)) / xyz.shape[2]

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return (self.lower_limit, self.upper_limit)
