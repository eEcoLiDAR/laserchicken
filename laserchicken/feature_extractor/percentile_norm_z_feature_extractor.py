from laserchicken.feature_extractor import PercentileZFeatureExtractor
from laserchicken.keys import normalized_height

PERCENTILES = range(10, 110, 10)


class PercentileNormZFeatureExtractor(PercentileZFeatureExtractor):
    """Height percentiles feature extractor class."""
    DATA_KEY = normalized_height

    @classmethod
    def provides(cls):
        """
        Get a list of names of the feature values.

        This will return as many names as the number feature values that will be returned.
        For instance, if a feature extractor returns the first 3 Eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        return ['perc_{}_norm_z'.format(i) for i in PERCENTILES]
