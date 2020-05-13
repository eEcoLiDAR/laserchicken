import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class RangeFeatureExtractor(FeatureExtractor):
    """Calculates the max, min and range on the z axis."""

    DEFAULT_MAX = float('NaN')
    DEFAULT_MIN = float('NaN')

    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        base_names = ['max_', 'min_', 'range_']
        return [base + str(self.data_key) for base in base_names]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return np.array([self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]).T

    def _extract_one(self, source_point_cloud, neighborhood):
        if neighborhood:
            source_data = source_point_cloud[point][self.data_key]['data'][neighborhood]
            max_z = np.max(source_data) if len(source_data) > 0 else self.DEFAULT_MAX
            min_z = np.min(source_data) if len(source_data) > 0 else self.DEFAULT_MIN
            range_z = max_z - min_z
        else:
            max_z = min_z = range_z = np.NaN
        return max_z, min_z, range_z
