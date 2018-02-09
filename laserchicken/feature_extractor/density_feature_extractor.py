from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point
from laserchicken.volume_specification import Sphere, InfiniteCylinder


class PointDensityFeatureExtractor(AbstractFeatureExtractor):
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

        if sourcepc is not None and isinstance(neighborhood, list):
            npts = float(len(sourcepc[point]['x']['data'][neighborhood]))

        elif targetpc is not None:
            npts = float(len(targetpc[point]['x']['data']))
        else:
            raise ValueError("You can either specify a sourcepc and a neighborhhod or a targetpc\n\
                              example\nextractror.extract(sourcepc,index,None,None,volume)\n\
                              extractror.extract(None,None,targetpc,None,volume)")

        # sphere/cylinder cases
        if volume.get_type() == Sphere.TYPE:
            vol = volume.calculate_volume()
            return npts / vol

        elif volume.get_type() == InfiniteCylinder.TYPE:
            area = volume.calculate_base_area()
            return npts / area

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return ()
