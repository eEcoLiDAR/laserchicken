import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class HeightStatisticsFeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['max_z', 'min_z', 'mean_z', 'median_z', 'std_z', 'var_z', 'range', 'coeff_var_z', 'skew_z', 'kurto_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex):
        z = sourcepc[point]['z']['data'][neighborhood]
        max_z = np.max(z)
        min_z = np.min(z)
        mean_z = np.mean(z)
        median_z = np.median(z)
        std_z = np.std(z)
        var_z = np.var(z)
        range_z = max_z - min_z
        coeff_var_z = np.std(z) / np.mean(z)
        skew_z = stat.skew(z)
        kurto_z = stat.kurtosis(z)
        return max_z, min_z, mean_z, median_z, std_z, var_z, range_z, coeff_var_z, skew_z, kurto_z
