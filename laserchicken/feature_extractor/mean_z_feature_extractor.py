import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class MeanZFeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['max_z', 'min_z', 'mean_z', 'median_z', 'std_z', 'var_z', 'range', 'coeff_var_z', 'skew_z', 'kurto_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            mean_z = np.mean(z)
        else:
            mean_z = np.NaN
        return mean_z
