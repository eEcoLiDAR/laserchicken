import importlib
import re

from .density_feature_extractor import PointDensityFeatureExtractor
from .echo_ratio_feature_extractor import EchoRatioFeatureExtractor
from .eigenvals_feature_extractor import EigenValueVectorizeFeatureExtractor
from .entropy_z_feature_extractor import EntropyZFeatureExtractor
from .percentile_z_feature_extractor import PercentileZFeatureExtractor
from .pulse_penetration_feature_extractor import PulsePenetrationFeatureExtractor
from .sigma_z_feature_extractor import SigmaZFeatureExtractor
from .median_z_feature_extractor import MedianZFeatureExtractor
from .range_z_feature_extractor import RangeZFeatureExtractor
from .var_z_feature_extractor import VarianceZFeatureExtractor
from .mean_std_coeff_z_feature_extractor import MeanStdCoeffZFeatureExtractor
from .skew_z_feature_extractor import SkewZFeatureExtractor
from .kurtosis_z_feature_extractor import KurtosisZFeatureExtractor
from .skew_norm_z_feature_extractor import SkewNormZFeatureExtractor
from .mean_std_coeff_norm_z_feature_extractor import MeanStdCoeffNormZFeatureExtractor
from .var_norm_z_feature_extractor import VarianceNormZFeatureExtractor
from .range_norm_z_feature_extractor import RangeNormZFeatureExtractor
from .kurtosis_norm_z_feature_extractor import KurtosisNormZFeatureExtractor
from .entropy_norm_z_feature_extractor import EntropyNormZFeatureExtractor
from .median_norm_z_feature_extractor import MedianNormZFeatureExtractor
from .percentile_norm_z_feature_extractor import PercentileNormZFeatureExtractor
from .density_absolute_mean_z_feature_extractor import DensityAbsoluteMeanZFeatureExtractor
from .density_absolute_mean_norm_z_feature_extractor import DensityAbsoluteMeanNormZFeatureExtractor

def create_default_feature_map(module_name=__name__):
    """Construct a mapping from feature names to feature extractor classes."""
    name_extractor_pairs = _find_name_extractor_pairs(module_name)
    return {feature_name: extractor for feature_name, extractor in name_extractor_pairs}


def _find_name_extractor_pairs(module_name):
    module = importlib.import_module(module_name)
    name_extractor_pairs = [(feature_name, extractor)
                            for name, extractor in vars(module).items() if
                            re.match('^[A-Z][a-zA-Z0-9_]*FeatureExtractor$', name)
                            for feature_name in extractor.provides()]
    return name_extractor_pairs