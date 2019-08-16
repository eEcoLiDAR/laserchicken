import numpy as np

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.utils import get_xyz


class EigenValueVectorizeFeatureExtractor(AbstractFeatureExtractor):
    is_vectorized = True

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['eigenv_1', 'eigenv_2', 'eigenv_3', 'normal_vector_1', 'normal_vector_2', 'normal_vector_3', 'slope']

    @staticmethod
    def _get_cov(xyz):
        n_max = xyz.shape[2]
        n = (xyz.mask.sum(axis=2, keepdims=True) * -1) + n_max
        m = xyz - xyz.sum(2, keepdims=True) / n
        return np.einsum('ijk,ilk->ijl', m, m) / (n - 1)

    def extract(self, sourcepc, neighborhoods, targetpc, targetindex, volume):
        if not (isinstance(neighborhoods[0], list) or isinstance(neighborhoods[0], range)):
            neighborhoods = [neighborhoods]

        xyz_grp = get_xyz(sourcepc, neighborhoods)
        self._mask_rows_with_too_few_points(xyz_grp)

        e_vals, eigvects = self._get_eigen_vals_and_vects(xyz_grp)
        normals = eigvects[:, :, 2]  # For all instances, take all elements of the 3th (smallest) vector.(normals, axis=1)
        alpha = np.arccos(np.dot(normals, np.array([0., 0., 1.])))
        slope = np.tan(alpha)

        return e_vals[:, 0], e_vals[:, 1], e_vals[:, 2], normals[:, 0], normals[:, 1], normals[:, 2], slope

    def _get_eigen_vals_and_vects(self, xyz_grp):
        cov_mat = self._get_cov(xyz_grp)
        eigval, eigvects = np.linalg.eig(cov_mat)
        e = np.sort(eigval, axis=1)[:, ::-1]  # Sorting to make result identical to serial implementation.
        return e, eigvects
        # indices = sorted(range(eigval.shape[1]), key=lambda i: eigval[:, i], reverse=True)
        # return eigval[:,indices], eigvects[:,:,indices]

    @staticmethod
    def _mask_rows_with_too_few_points(xyz_grp):
        minimum_for_calculation = 3
        invalid_cells = xyz_grp.mask == False
        invalid_neighbors = np.any(invalid_cells, axis=1)
        invalid_rows = np.sum(invalid_neighbors, axis=1) < minimum_for_calculation
        xyz_grp.mask[invalid_rows, :, :] = True
