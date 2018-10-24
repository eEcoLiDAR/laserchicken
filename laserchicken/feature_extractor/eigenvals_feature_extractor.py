import numpy as np

from laserchicken import utils
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.utils import get_xyz


def _structure_tensor(points):
    """
    Computes the structure tensor of points by computing the eigenvalues
    and eigenvectors of the covariance matrix of a point cloud.
    Parameters
    ----------
    points : (Mx3) array
        X, Y and Z coordinates of points.
    Returns
    -------
    eigenvalues : (1x3) array
        The eigenvalues corresponding to the eigenvectors of the covariance
        matrix.
    eigenvectors : (3,3) array
        The eigenvectors of the covariance matrix.
    """
    if points.shape[0] > 3:
        cov_mat = np.cov(points, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eig(cov_mat)
        order = np.argsort(-eigenvalues)
        eigenvalues = eigenvalues[order]
        eigenvectors = eigenvectors[:, order]
        return eigenvalues, eigenvectors
    else:
        raise ValueError('Not enough points to compute eigenvalues/vectors.')


class EigenValueOld(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ["eigenv_1", "eigenv_2", "eigenv_3"]

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        nbptsX, nbptsY, nbptsZ = utils.get_point(sourcepc, neighborhood)
        matrix = np.column_stack((nbptsX, nbptsY, nbptsZ))

        try:
            eigenvals, eigenvecs = _structure_tensor(matrix)
        except ValueError as err:
            if str(err) == 'Not enough points to compute eigenvalues/vectors.':
                return [0, 0, 0]
            else:
                raise

        return [eigenvals[0], eigenvals[1], eigenvals[2]]


class EigenValueVectorizeFeatureExtractor(AbstractFeatureExtractor):
    is_vectorized = True

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['eigenv_1', 'eigenv_2', 'eigenv_3']

    @staticmethod
    def _get_cov(xyz):
        n_max = xyz.shape[2]
        n = (xyz.mask.sum(axis=2, keepdims=True) * -1) + n_max
        m = xyz - xyz.sum(2, keepdims=True) / n
        return np.einsum('ijk,ilk->ijl', m, m) / (n - 1)

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        if not isinstance(neighborhood[0], list):
            neighborhood = [neighborhood]

        xyz_grp = get_xyz(sourcepc, neighborhood)
        cov_mat = self._get_cov(xyz_grp)

        eigval, eigvects = np.linalg.eig(cov_mat)

        e = np.sort(eigval, axis=1)[:, ::-1]  # Sorting to make result identical to serial implementation.
        print(eigvects)
        normals = eigvects[:, :, 2]
        print(normals)
        slope = np.dot(normals, np.array([0., 0., 1.]))

        return e[:, 0], e[:, 1], e[:, 2], normals[:, 0], normals[:, 1], normals[:, 2], slope
