import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class KurtosisFeatureExtractor(FeatureExtractor):
    """Calculates the variation on the z axis."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return ['kurto_' + self.data_key]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return [self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]

    def _extract_one(self, sourcepc, neighborhood):
        if neighborhood:
            z = sourcepc[point][self.data_key]['data'][neighborhood]
            kurtosis_z = stat.kurtosis(z)
        else:
            kurtosis_z = np.NaN
        return kurtosis_z
