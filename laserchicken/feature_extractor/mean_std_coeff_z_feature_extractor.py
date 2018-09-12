import numpy as np

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class MeanStdCoeffZFeatureExtractor(AbstractFeatureExtractor):
    """Calculates mean, standard deviation and the ration between the two."""

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['mean_z', 'std_z', 'coeff_var_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            mean_z = np.mean(z)
            std_z = np.std(z)
            coeff_var_z = std_z / mean_z
        else:
            mean_z = std_z = coeff_var_z = np.NaN
        return mean_z, std_z, coeff_var_z
