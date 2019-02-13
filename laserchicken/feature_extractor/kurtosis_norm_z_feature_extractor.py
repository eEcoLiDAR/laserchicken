from laserchicken import keys
from laserchicken.feature_extractor import KurtosisZFeatureExtractor


class KurtosisNormZFeatureExtractor(KurtosisZFeatureExtractor):
    """Calculates the variation on the normalized height."""
    DATA_KEY = keys.normalized_height

    @classmethod
    def provides(cls):
        return ['kurto_norm_z']
