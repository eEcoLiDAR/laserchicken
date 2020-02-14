"""Sigma Z feature extractor.

Here, Sigma Z is defined as the standard deviation of the residuals after plane fitting.
See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/20
"""
import numpy as np
from numpy.linalg import LinAlgError

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.utils import get_point, fit_plane


class SigmaZFeatureExtractor(FeatureExtractor):
    """Height percentiles feature extractor class."""

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
        return ['sigma_z']

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

    @staticmethod
    def _extract_one(source_point_cloud, neighborhood):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param source_point_cloud: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :return:
        """
        x, y, z = get_point(source_point_cloud, neighborhood)
        try:
            plane_estimator = fit_plane(x, y, z)
            normalized = z - plane_estimator(x, y)
            return np.std(normalized)
        except LinAlgError:
            return 0

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractor object.

        Needed for provenance.
        """
        return ()
