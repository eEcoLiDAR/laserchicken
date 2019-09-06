import numpy as np

from laserchicken.feature_extractor.abc import FeatureExtractor
from laserchicken.keys import point


class MedianZFeatureExtractor(FeatureExtractor):
    """Calculates the median on the z axis."""
    DATA_KEY = 'z'

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['median_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point][self.DATA_KEY]['data'][neighborhood]
            median_z = np.median(z)
        else:
            median_z = np.NaN
        return median_z
