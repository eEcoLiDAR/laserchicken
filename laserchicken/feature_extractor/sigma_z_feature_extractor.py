"""Sigma Z feature extractor.

Here, Sigma Z is defined as the standard deviation of the residuals after plane fitting.
See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/20
"""
import numpy as np
from numpy.linalg import LinAlgError

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor

from laserchicken.utils import get_xyz_per_neighborhood

class SigmaZFeatureExtractor(FeatureExtractor):
    """Height percentiles feature extractor class."""
    is_vectorized = True

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
        return ['sigma_z']

    def extract(self, source_point_cloud, neighborhoods, target_point_cloud, target_index, volume_description):
        """
        Extract the feature value(s) of the point cloud at location of the target.

        :param source_point_cloud: environment (search space) point cloud
        :param neighborhood: array of indices of points within the point_cloud argument
        :param target_point_cloud: point cloud that contains target point
        :param target_index: index of the target point in the target point cloud
        :param volume_description: volume object describing the containing volume of the neighborhood
        :return:
        """
        if not (isinstance(neighborhoods[0], list) or isinstance(neighborhoods[0], range)):
            neighborhoods = [neighborhoods]

        xyz_grp = get_xyz_per_neighborhood(source_point_cloud, neighborhoods)
        len_ngbrs = [len(ngbr) for ngbr in neighborhoods]

        try:
            residuals = self._get_sum_of_residuals_from_fitted_planes(xyz_grp)
            return np.sqrt(np.divide(residuals, len_ngbrs))
        except LinAlgError:
            return 0

    @staticmethod
    def _get_sum_of_residuals_from_fitted_planes(xyz):
        """
        Fit planes to each of the neighborhoods and returns the corresponding sum of residuals
        :param xyz: 3D masked array with (x,y,z) of points in neighboroods.
        :return: array with residuals
        """
        # setup coefficient matrices and ordinate values
        matrix = np.ones_like(xyz)
        matrix[:, 1:, :] = xyz[:, 0:2, :]
        matrix[xyz.mask] = 0.
        matrix = np.transpose(matrix, (0, 2, 1))
        a = np.zeros((xyz.shape[0], xyz.shape[2]))
        a[:, :] = xyz[:, 2, :]

        # SVD decomposition of matrices to construct pseudo-inverse
        u, s, v = np.linalg.svd(matrix, full_matrices=False)

        # find matrices with zero-singular values, and solve linear problems
        zero_sing_val_mask = np.any(np.isclose(s, 0.), axis=1)
        inv_s = np.zeros_like(s)
        inv_s[~zero_sing_val_mask, :] = 1 / s[~zero_sing_val_mask, :]
        parameters = np.einsum('ijk,ij->ik', v,
                               inv_s * np.einsum('ijk,ij->ik', u, a))

        # determine residuals for non-singular matrices, set others to zero
        a_val = np.einsum('ijk,ik->ij', matrix, parameters)
        residuals = np.sum(np.power(a - a_val, 2), axis=1)
        residuals[zero_sing_val_mask] = 0.
        return residuals

    def get_params(self):
        """
        Return a tuple of parameters involved in the current feature extractor object.

        Needed for provenance.
        """
        return ()
