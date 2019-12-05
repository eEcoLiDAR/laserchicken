"""Abstract feature extractor."""


class FeatureExtractor(object):
    """Abstract feature extractor class."""

    @classmethod
    def requires(cls):
        """
        Get a list of names of the point attributes that are needed for this feature extraction.

        For simple features, this could be just x, y, and z. Other features can build on again
        other features to have been computed first.

        :return: List of feature names
        """
        raise NotImplementedError(
            "Class %s doesn't implement get_requirements()" % (cls.__name__))

    @classmethod
    def provides(cls):
        """
        Get a list of names of the feature values.

        This will return as many names as the number feature values that will be returned.
        For instance, if a feature extractor returns the first 3 Eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.

        :return: List of feature names
        """
        raise NotImplementedError(
            "Class %s doesn't implement get_names()" % (cls.__name__))

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_index, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param point_cloud: environment (search space) point cloud
        :param neighborhoods: list of arrays of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_indices: list of indices of the target point in the target point cloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature values
        """
        raise NotImplementedError(
            "Class %s doesn't implement extract_features()" % (self.__class__.__name__))

    def get_params(self):
        """
        Returns a tuple of parameters involved in the current feature extractor
        object. Needed for provenance.
        """
        return ()


