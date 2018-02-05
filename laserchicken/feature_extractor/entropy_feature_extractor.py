"""Shannan entropy calculation. For more info see https://rdrr.io/cran/lidR/man/entropy.html"""

import numpy as np
from laserchicken import keys
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor


class EntropyFeatureExtractor(AbstractFeatureExtractor):
    # TODO: make this settable from command line
    layer_thickness = 0.5
    z_min = None
    z_max = None

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['z_entropy']

    def get_params(self):
        p = [self.layer_thickness]
        if self.z_min is not None:
            p.append(self.z_min)
        if self.z_max is not None:
            p.append(self.z_max)
        return p

    def extract(self, source_pc, neighborhood, target_pc, target_index):
        z = source_pc[keys.point]["z"]["data"][neighborhood]
        _z_min = np.min(z) if self.z_min is None else self.z_min
        _z_max = np.max(z) if self.z_max is None else self.z_max
        n_bins = int(np.ceil((_z_max - _z_min) / self.layer_thickness))
        data = np.histogram(z, bins=n_bins, range=(_z_min, _z_max), density=True)[0]
        entropy_func = np.vectorize(_x_log_2x)
        norm = np.sum(data)
        return -(entropy_func(data / norm)).sum()


def _x_log_2x(x):
    return 0 if x == 0 else x * np.log2(x)
