import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class MedianFeatureExtractor(FeatureExtractor):
    """Calculates the median on the z axis."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return ['median_' + self.data_key]

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            source_data = sourcepc[point][self.data_key]['data'][neighborhood]
            median = np.median(source_data)
        else:
            median = np.NaN
        return median
