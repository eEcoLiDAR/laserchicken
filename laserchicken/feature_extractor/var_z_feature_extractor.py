import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class VarianceZFeatureExtractor(FeatureExtractor):
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
