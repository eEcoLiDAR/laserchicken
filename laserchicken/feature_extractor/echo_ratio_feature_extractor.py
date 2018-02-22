from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point
import numpy as np
class EchoRatioFeatureExtractor(AbstractFeatureExtractor):
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
        return ['echo_ratio']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param point_cloud: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_index: index of the target point in the target pointcloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature value
        """

        if volume.TYPE != 'infinite cylinder':
            raise ValueError('The volume must be a cylinder')

        if targetpc is None:
            raise ValueError('Target point cloud required')

        if targetindex is None:
            raise ValueError('Target point index required')

        # get the xyz of the cylinder neighborhood
        x = sourcepc[point]['x']['data'][neighborhood]
        y = sourcepc[point]['y']['data'][neighborhood]
        z = sourcepc[point]['z']['data'][neighborhood]
        xyz = np.column_stack((x,y,z))
        ncyl = xyz.shape[0]

        # get the position of the target point
        x0 = targetpc[point]['x']['data'][targetindex]
        y0 = targetpc[point]['y']['data'][targetindex]
        z0 = targetpc[point]['z']['data'][targetindex]
        xyz0 = np.array([x0,y0,z0])

        # get the number of point in the sphere
        nsphere = np.sum(np.sum((xyz-xyz0)**2,1)<=volume.radius**2)

        return nsphere / ncyl * 100.

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return ()
