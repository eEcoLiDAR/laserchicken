from laserchicken.feature_extractor.percentile_z_feature_extractor import PercentileZFeatureExtractor
from laserchicken.keys import normalized_height


class PercentileNormZFeatureExtractor(PercentileZFeatureExtractor):
    """Normalized height percentiles for feature extractor class."""
    DATA_KEY = normalized_height
