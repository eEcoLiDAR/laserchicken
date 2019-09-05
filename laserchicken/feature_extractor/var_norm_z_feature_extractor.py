from laserchicken import keys
from laserchicken.feature_extractor.var_z_feature_extractor import VarianceZFeatureExtractor


class VarianceNormZFeatureExtractor(VarianceZFeatureExtractor):
    """Calculates the variation on the z axis."""
    DATA_KEY = keys.normalized_height

    @classmethod
    def provides(cls):
        return ['var_norm_z']

