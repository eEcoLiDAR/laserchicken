from laserchicken import keys
from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
from .density_absolute_mean_feature_extractor import DensityAbsoluteMeanFeatureExtractor
from .density_feature_extractor import PointDensityFeatureExtractor
from .echo_ratio_feature_extractor import EchoRatioFeatureExtractor
from .eigenvals_feature_extractor import EigenValueVectorizeFeatureExtractor
from .entropy_feature_extractor import EntropyFeatureExtractor
from .kurtosis_feature_extractor import KurtosisFeatureExtractor
from .mean_std_coeff_feature_extractor import MeanStdCoeffFeatureExtractor
from .median_feature_extractor import MedianFeatureExtractor
from .percentile_feature_extractor import PercentileFeatureExtractor
from .pulse_penetration_feature_extractor import PulsePenetrationFeatureExtractor
from .range_feature_extractor import RangeFeatureExtractor
from .sigma_z_feature_extractor import SigmaZFeatureExtractor
from .skew_feature_extractor import SkewFeatureExtractor
from .var_feature_extractor import VarianceFeatureExtractor


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
            EntropyFeatureExtractor(),
            EntropyFeatureExtractor(data_key=keys.normalized_height),
            PulsePenetrationFeatureExtractor(),
            SigmaZFeatureExtractor(),
            MedianFeatureExtractor(),
            MedianFeatureExtractor(data_key=keys.normalized_height),
            VarianceFeatureExtractor(),
            VarianceFeatureExtractor(data_key=keys.normalized_height),
            MeanStdCoeffFeatureExtractor(),
            MeanStdCoeffFeatureExtractor(data_key=keys.normalized_height),
            MeanStdCoeffFeatureExtractor(data_key=keys.intensity),
            SkewFeatureExtractor(),
            SkewFeatureExtractor(data_key=keys.normalized_height),
            KurtosisFeatureExtractor(),
            KurtosisFeatureExtractor(data_key=keys.normalized_height),
            RangeFeatureExtractor(),
            RangeFeatureExtractor(data_key=keys.normalized_height),
            RangeFeatureExtractor(data_key=keys.intensity),
            DensityAbsoluteMeanFeatureExtractor(),
            DensityAbsoluteMeanFeatureExtractor(data_key=keys.normalized_height),
            BandRatioFeatureExtractor(None, 1, data_key=keys.normalized_height),
            BandRatioFeatureExtractor(1, 2, data_key=keys.normalized_height),
            BandRatioFeatureExtractor(2, 3, data_key=keys.normalized_height),
            BandRatioFeatureExtractor(3, None, data_key=keys.normalized_height)] \
           + [PercentileFeatureExtractor(percentile=p) for p in range(1, 101)] \
           + [PercentileFeatureExtractor(percentile=p, data_key=keys.normalized_height) for p in range(1, 101)]
