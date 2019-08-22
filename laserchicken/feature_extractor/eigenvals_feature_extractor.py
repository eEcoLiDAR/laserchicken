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
        normals = eigvects[:, :, 2]  # For all instances, take all elements of the 3th vector (= normal vector).
        alpha = np.arccos(np.dot(normals, np.array([0., 0., 1.])))
        slope = np.tan(alpha)

        return e_vals[:, 0], e_vals[:, 1], e_vals[:, 2], normals[:, 0], normals[:, 1], normals[:, 2], slope

    def _get_eigen_vals_and_vects(self, xyz_grp):
        cov_mat = self._get_cov(xyz_grp)
        eigval, eigvects = np.linalg.eig(cov_mat)
        return self._sort(eigval, eigvects)

    def _sort(self, eigval, eigvects):
        val_indices = np.argsort(eigval, axis=1)[:, ::-1]
        ordered_vects = self._reorder_vects(eigvects, val_indices)
        ordered_eigval = np.take_along_axis(eigval, val_indices, axis=1)
        return ordered_eigval, ordered_vects

    @staticmethod
    def _reorder_vects_old(eigvects, new_vector_indices):
        """
        Swaps the order of the eigen vectors according to the given new indices. Note that each single vector is kept
        unchanged.
        :param eigvects:
        :param new_vector_indices:
        :return: The input eigen vectors in their new order.
        """
        # I'm reordering vectors in the last two dimensions while keeping the first dimension unchanged. I can't find
        # any existing functions that do this exactly the way it needs to be sorted. Therefore I have to transpose
        # and reshape and even repeat some indices to get the behavior I'm looking for.
        vects_t = eigvects.transpose([0, 2, 1])  # The eigen vectors used to be column vectors. Making row vectors here.
        flattened_vects_t = vects_t.reshape(-1, 3 * 3)  # Flatten the (eigen) vector dimension
        vect_indices = np.zeros_like(flattened_vects_t, dtype=np.int) + [0, 1, 2, 0, 1, 2, 0, 1, 2]  # 0,1,2 for x,y,z
        vect_indices[:, :3] += new_vector_indices[:, 0:1] * 3  # Because x,y,z, indices have to be increased by 3.
        vect_indices[:, 3:6] += new_vector_indices[:, 1:2] * 3
        vect_indices[:, 6:9] += new_vector_indices[:, 2:3] * 3
        ordered_flattened_vects_t = np.take_along_axis(flattened_vects_t, vect_indices, axis=1)
        ordered_vects_t = ordered_flattened_vects_t.reshape(eigvects.shape)
        ordered_vects = ordered_vects_t
        return ordered_vects.transpose([0, 2, 1])

    @staticmethod
    def _mask_rows_with_too_few_points(xyz_grp):
        minimum_for_calculation = 3
        invalid_cells = xyz_grp.mask == False
        invalid_neighbors = np.any(invalid_cells, axis=1)
        invalid_rows = np.sum(invalid_neighbors, axis=1) < minimum_for_calculation
        xyz_grp.mask[invalid_rows, :, :] = True
