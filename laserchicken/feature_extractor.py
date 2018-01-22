class FeatureExtractor(object):
    def get_requirements(self):
        """
        Get a list of names of the point attributes that are needed for this feature extraction. For simple features,
        this could be just x, y, and z. Other features can build on again other features to have been computed first.
        :return: List of feature names
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

    def get_names(self):
        """
        Get a list of names of the feature values. This will return as many names as as the number feature values
        that will be returned. For instance, if a feature extractor returns the first 3 Eigen values, this method
        should return 3 names, for instance 'eigen_value_1', 'eigen_value_2' and 'eigen_value_3'.
        :return: List of feature names
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

    def extract_features(self, point_cloud, target):
        """
        Extract the feature value(s) of the point cloud at location of the target.
        :param point_cloud:
        :param target:
        :return:
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))
