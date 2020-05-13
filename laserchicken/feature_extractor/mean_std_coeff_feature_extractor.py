import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class MeanStdCoeffFeatureExtractor(FeatureExtractor):
    """Calculates mean, standard deviation and the ratio between the two."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        base_names = ['mean_', 'std_', 'coeff_var_']
        return [base + str(self.data_key) for base in base_names]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return np.array([self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]).T

    def _extract_one(self, sourcepc, neighborhood):
        if neighborhood:
            z = sourcepc[point][self.data_key]['data'][neighborhood]
            mean_z = np.mean(z)
            std_z = np.std(z)
            coeff_var_z = std_z / mean_z
        else:
            mean_z = std_z = coeff_var_z = np.NaN
        return mean_z, std_z, coeff_var_z
