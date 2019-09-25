from laserchicken import keys
from laserchicken.feature_extractor.mean_std_coeff_z_feature_extractor import MeanStdCoeffZFeatureExtractor


class MeanStdCoeffNormZFeatureExtractor(MeanStdCoeffZFeatureExtractor):
    """Calculates mean, standard deviation of the normalized height and the ratio between the two."""
    DATA_KEY = keys.normalized_height

    @classmethod
    def provides(cls):
        return ['mean_norm_z', 'std_norm_z', 'coeff_var_norm_z']
