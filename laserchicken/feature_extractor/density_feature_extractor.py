from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point
from laserchicken.volume_specification import Sphere, InfiniteCylinder


class PointDensityFeatureExtractor(FeatureExtractor):
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
        return ['point_density']

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
        return [self._extract_one(point_cloud, neighborhood, volume_description) for neighborhood in neighborhoods]

    def _extract_one(self, source_pc, neighborhood, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param source_pc: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature value
        """
        n_points = len(source_pc[point]['x']['data'][neighborhood])
        area_or_volume = volume_description.calculate_area_or_volume()
        return float(n_points) / area_or_volume

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return ()
