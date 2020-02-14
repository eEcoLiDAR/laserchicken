import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class SkewFeatureExtractor(FeatureExtractor):
    """Calculates the skew on the z axis."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return ['skew_' + self.data_key]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return [self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]

    def _extract_one(self, point_cloud, neighborhood):
        if neighborhood:
            source_data = point_cloud[point][self.data_key]['data'][neighborhood]
            skew = stat.skew(source_data)
        else:
            skew = np.NaN
        return skew
