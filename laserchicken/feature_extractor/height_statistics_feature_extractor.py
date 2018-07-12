import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class HeightStatisticsFeatureExtractor(AbstractFeatureExtractor):
    DEFAULT_MAX = float('NaN')
    DEFAULT_MIN = float('NaN')

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['max_z', 'min_z', 'mean_z', 'median_z', 'std_z', 'var_z', 'range', 'coeff_var_z', 'skew_z', 'kurto_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            max_z = np.max(z) if len(z) > 0 else self.DEFAULT_MAX
            min_z = np.min(z) if len(z) > 0 else self.DEFAULT_MIN
            mean_z = np.mean(z)
            median_z = np.median(z)
            std_z = np.std(z)
            var_z = np.var(z)
            range_z = max_z - min_z
            coeff_var_z = np.std(z) / np.mean(z)
            skew_z = stat.skew(z)
            kurto_z = stat.kurtosis(z)
        else:
            max_z = min_z = mean_z = median_z = std_z = var_z = range_z = coeff_var_z = skew_z = kurto_z = np.NaN
        return max_z, min_z, mean_z, median_z, std_z, var_z, range_z, coeff_var_z, skew_z, kurto_z
