import numpy as np
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point
from laserchicken.utils import fit_plane_svd


class NormalPlaneFeatureExtractor(AbstractFeatureExtractor):
    """Feature extractor for the normal and slope of a plane."""

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
        return ['normal_vector_1', 'normal_vector_2', 'normal_vector_3', 'slope']

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

        x = _to_float64(point_cloud[point]['x']['data'][neighborhood])
        y = _to_float64(point_cloud[point]['y']['data'][neighborhood])
        z = _to_float64(point_cloud[point]['z']['data'][neighborhood])

        try:
            normal_vector = fit_plane_svd(x, y, z)
            slope = np.dot(normal_vector, np.array([0., 0., 1.]))
        except np.linalg.linalg.LinAlgError:
            normal_vector = [0.0, 0.0, 0.0]
            slope = 0.0

        return normal_vector[0], normal_vector[1], normal_vector[2], slope

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return ()


def _to_float64(x_org):
    """
    Returns the input if dtype is float64 or a copy of it with this dtype if it isn't.
    NB. Returns reference to input array or copy.
    :param x_org:
    :return: array with float64 dtype
    """
    return x_org if x_org.dtype == np.float64 else np.array(x_org, dtype=np.float64)
