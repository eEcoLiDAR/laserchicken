import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class MaxZFeatureExtractor(AbstractFeatureExtractor):
    """Extracts the maximum value on the z axis."""
    DEFAULT_MAX = float('NaN')

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['max_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            max_z = np.max(z) if len(z) > 0 else self.DEFAULT_MAX
        else:
            max_z = np.NaN
        return max_z
