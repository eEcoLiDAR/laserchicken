from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point
from laserchicken.volume_specification import Sphere, InfiniteCylinder


class PulsePenetraionFeatureExtractor(AbstractFeatureExtractor):
    """Feature extractor for the point density."""

    #classification according to
    #http://www.asprs.org/wp-content/uploads/2010/12/LAS_1-4_R6.pdf

    points_class = {'ground':[2],'vegetation':[3,4,5]}

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
        return ['pulse_penetration_ratio','density_absolute_mean']

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

        # get the raw classification
        classdata = sourcepc[point]['raw_classification']['data']

        # get the indexes
        index_veg = [ c for c in classdata for veg in self.points_class['vegetation'] if c == veg ]
        index_grd = [ c for c in classdata for veg in self.points_class['ground'] if c == veg ]

        # size
        nveg,ngrd,ntot = len(index_veg), len(index_grd), len(classdata)

        # puls penetration ratio
        pulse_penetration_ratio = ngrd/ntot

        # ground heights
        zgrd = sourcepc[point]['z']['data'][index_grd]
        density_absolute_mean = len(zgrd[zgrd>np.mean(zgrd)]) / ngrd * 100.

        return pulse_penetration_ratio, density_absolute_mean

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractorobject.

        Needed for provenance.
        """
        return ()
