from laserchicken.feature_extractor.median_z_feature_extractor import MedianZFeatureExtractor
from laserchicken.keys import normalized_height


class MedianNormZFeatureExtractor(MedianZFeatureExtractor):
    """Calculates the median on the normalized height."""
    DATA_KEY = normalized_height

    @classmethod
    def provides(cls):
        return ['median_norm_z']
