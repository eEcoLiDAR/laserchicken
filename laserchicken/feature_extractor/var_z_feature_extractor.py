import numpy as np

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class VarianceZFeatureExtractor(AbstractFeatureExtractor):
    """Calculates the variation on the z axis."""
    DATA_KEY = 'z'

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['var_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point][self.DATA_KEY]['data'][neighborhood]
            var_z = np.var(z)
        else:
            var_z = np.NaN
        return var_z
