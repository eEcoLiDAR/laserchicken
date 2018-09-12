import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class VariationZFeatureExtractor(AbstractFeatureExtractor):
    """Calculates the variation on the z axis."""
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['var_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            std_z = np.var(z)
        else:
            std_z = np.NaN
        return std_z
