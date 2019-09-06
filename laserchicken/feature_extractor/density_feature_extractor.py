from laserchicken.feature_extractor.abc import FeatureExtractor
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

    def extract(self, source_pc, neighborhood, target_pc, target_index, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param source_pc: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :param target_pc: point cloud that contains target point
        :param target_index: index of the target point in the target pointcloud
        :param volume_description: volume object that describes the shape and size of the search volume
        :return: feature value
        """

        if source_pc is not None and isinstance(neighborhood, list):
            n_points = float(len(source_pc[point]['x']['data'][neighborhood]))

        elif target_pc is not None:
            n_points = float(len(target_pc[point]['x']['data']))
        else:
            raise ValueError("You can either specify a sourcepc and a neighborhood or a targetpc\n\
                              example\nextractror.extract(sourcepc,index,None,None,volume)\n\
                              extractror.extract(None,None,targetpc,None,volume)")

        area_or_volume = volume_description.calculate_area_or_volume()
        return n_points / area_or_volume



    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return ()
