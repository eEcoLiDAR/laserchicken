"""Shannan entropy calculation. For more info see https://rdrr.io/cran/lidR/man/entropy.html"""

import numpy as np
from laserchicken import keys
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor


class EntropyFeatureExtractor(FeatureExtractor):
    layer_thickness = 0.5
    min_val = None
    max_val = None

    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return ['entropy_' + self.data_key]

    def get_params(self):
        return [self.layer_thickness, self.min_val, self.max_val]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume):
        return [self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]

    def _extract_one(self, source_pc, neighborhood):
        if len(neighborhood) == 0:
            return 0
        source_data = source_pc[keys.point][self.data_key]["data"][neighborhood]
        data_min = np.min(source_data) if self.min_val is None else self.min_val
        data_max = np.max(source_data) if self.max_val is None else self.max_val
        if data_min == data_max:
            return 0
        n_bins = int(np.ceil((data_max - data_min) / self.layer_thickness))
        data = np.histogram(source_data, bins=n_bins, range=(data_min, data_max), density=True)[0]
        entropy_func = np.vectorize(_x_log_2x)
        norm = np.sum(data)
        return -(entropy_func(data / norm)).sum()


def _x_log_2x(x):
    return 0 if x == 0 else x * np.log2(x)
