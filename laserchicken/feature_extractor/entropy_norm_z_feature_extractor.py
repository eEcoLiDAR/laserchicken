"""Shannan entropy calculation. For more info see https://rdrr.io/cran/lidR/man/entropy.html"""

from laserchicken import keys
from laserchicken.feature_extractor import EntropyZFeatureExtractor


class EntropyNormZFeatureExtractor(EntropyZFeatureExtractor):
    DATA_KEY = keys.normalized_height

    @classmethod
    def provides(cls):
        return ['entropy_norm_z']
