from laserchicken import keys
from laserchicken.feature_extractor import SkewZFeatureExtractor


class SkewNormZFeatureExtractor(SkewZFeatureExtractor):
    """Calculates the skew on the normalized height."""
    DATA_KEY = keys.normalized_height

    @classmethod
    def provides(cls):
        return ['skew_norm_z']
