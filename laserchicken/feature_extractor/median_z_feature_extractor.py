import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class MedianZFeatureExtractor(AbstractFeatureExtractor):
    """Calculates the median on the z axis."""
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['median_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            median_z = np.median(z)
        else:
            median_z = np.NaN
        return median_z
