from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
from .density_absolute_mean_norm_z_feature_extractor import DensityAbsoluteMeanNormZFeatureExtractor
from .density_absolute_mean_z_feature_extractor import DensityAbsoluteMeanZFeatureExtractor
from .density_feature_extractor import PointDensityFeatureExtractor
from .echo_ratio_feature_extractor import EchoRatioFeatureExtractor
from .eigenvals_feature_extractor import EigenValueVectorizeFeatureExtractor
from .entropy_norm_z_feature_extractor import EntropyNormZFeatureExtractor
from .entropy_z_feature_extractor import EntropyZFeatureExtractor
from .kurtosis_norm_z_feature_extractor import KurtosisNormZFeatureExtractor
from .kurtosis_z_feature_extractor import KurtosisZFeatureExtractor
from .mean_std_coeff_norm_z_feature_extractor import MeanStdCoeffNormZFeatureExtractor
from .mean_std_coeff_z_feature_extractor import MeanStdCoeffZFeatureExtractor
from .median_norm_z_feature_extractor import MedianNormZFeatureExtractor
from .median_z_feature_extractor import MedianZFeatureExtractor
from .percentile_norm_z_feature_extractor import PercentileNormZFeatureExtractor
from .percentile_z_feature_extractor import PercentileZFeatureExtractor
from .pulse_penetration_feature_extractor import PulsePenetrationFeatureExtractor
from .range_norm_z_feature_extractor import RangeNormZFeatureExtractor
from .range_z_feature_extractor import RangeZFeatureExtractor
from .sigma_z_feature_extractor import SigmaZFeatureExtractor
from .skew_norm_z_feature_extractor import SkewNormZFeatureExtractor
from .skew_z_feature_extractor import SkewZFeatureExtractor
from .var_norm_z_feature_extractor import VarianceNormZFeatureExtractor
from .var_z_feature_extractor import VarianceZFeatureExtractor


def create_default_feature_map():
    """Construct a mapping from feature names to feature extractor classes."""
    extractors = _get_default_extractors()
    name_extractor_pairs = _create_name_extractor_pairs(extractors)
    return {feature_name: extractor for feature_name, extractor in name_extractor_pairs}


def _create_name_extractor_pairs(extractors=None):
    if extractors is None:
        extractors = _get_default_extractors()
    name_extractor_pairs = [(feature_name, extractor)
                            for extractor in extractors
                            for feature_name in extractor.provides()]
    return name_extractor_pairs


def _get_default_extractors():
    return [PointDensityFeatureExtractor(),
            EchoRatioFeatureExtractor(),
            EigenValueVectorizeFeatureExtractor(),
            EntropyZFeatureExtractor(),
            PercentileZFeatureExtractor(),
            PulsePenetrationFeatureExtractor(),
            SigmaZFeatureExtractor(),
            MedianZFeatureExtractor(),
            RangeZFeatureExtractor(),
            VarianceZFeatureExtractor(),
            MeanStdCoeffZFeatureExtractor(),
            SkewZFeatureExtractor(),
            KurtosisZFeatureExtractor(),
            SkewNormZFeatureExtractor(),
            MeanStdCoeffNormZFeatureExtractor(),
            VarianceNormZFeatureExtractor(),
            RangeNormZFeatureExtractor(),
            KurtosisNormZFeatureExtractor(),
            EntropyNormZFeatureExtractor(),
            MedianNormZFeatureExtractor(),
            PercentileNormZFeatureExtractor(),
            DensityAbsoluteMeanZFeatureExtractor(),
            DensityAbsoluteMeanNormZFeatureExtractor(),
            BandRatioFeatureExtractor(-100, 1),
            BandRatioFeatureExtractor(1, 2),
            BandRatioFeatureExtractor(2, 3)] \
           + [PercentileZFeatureExtractor(p) for p in range(1, 101)] \
           + [PercentileNormZFeatureExtractor(p) for p in range(1, 101)]
