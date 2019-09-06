import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import FeatureExtractor
from laserchicken.keys import point


class RangeZFeatureExtractor(FeatureExtractor):
    """Calculates the max, min and range and max on the z axis."""

    DEFAULT_MAX = float('NaN')
    DEFAULT_MIN = float('NaN')
    DATA_KEY = 'z'

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['max_z', 'min_z', 'range_z']

    def extract(self, source_point_cloud, neighborhood, target_point_cloud, target_index, volume_description):
        if neighborhood:
            z = source_point_cloud[point][self.DATA_KEY]['data'][neighborhood]
            max_z = np.max(z) if len(z) > 0 else self.DEFAULT_MAX
            min_z = np.min(z) if len(z) > 0 else self.DEFAULT_MIN
            range_z = max_z - min_z
        else:
            max_z = min_z = range_z = np.NaN
        return max_z, min_z, range_z
