import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class KurtosisZFeatureExtractor(AbstractFeatureExtractor):
    """Calculates the variation on the z axis."""
    DATA_KEY = 'z'

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['kurto_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point][self.DATA_KEY]['data'][neighborhood]
            kurtosis_z = stat.kurtosis(z)
        else:
            kurtosis_z = np.NaN
        return kurtosis_z
