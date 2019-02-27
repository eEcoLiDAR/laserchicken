from laserchicken.feature_extractor import RangeZFeatureExtractor
from laserchicken.keys import normalized_height


class RangeNormZFeatureExtractor(RangeZFeatureExtractor):
    """Calculates the max, min and range and max on the normalized z axis."""

    DATA_KEY = normalized_height

    @classmethod
    def provides(cls):
        return ['max_norm_z', 'min_norm_z', 'range_norm_z']
