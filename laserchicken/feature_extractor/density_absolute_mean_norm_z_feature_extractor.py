"""Pulse penetration ratio and density absolute mean calculations.

See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/23.
"""

import numpy as np

from laserchicken.feature_extractor.abc import FeatureExtractor
from laserchicken.feature_extractor.density_absolute_mean_z_feature_extractor import \
    DensityAbsoluteMeanZFeatureExtractor
from laserchicken.keys import point, normalized_height

# classification according to
# http://www.asprs.org/wp-content/uploads/2010/12/LAS_1-4_R6.pdf
GROUND_TAGS = [2]


class DensityAbsoluteMeanNormZFeatureExtractor(DensityAbsoluteMeanZFeatureExtractor):
    """Feature extractor for the point density."""
    DATA_KEY = normalized_height

    @classmethod
    def provides(cls):
        """
        Get a list of names of the feature values.

        This will return as many names as the number feature values that will be returned.
        For instance, if a feature extractor returns the first 3 eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        return ['density_absolute_mean_norm_z']
