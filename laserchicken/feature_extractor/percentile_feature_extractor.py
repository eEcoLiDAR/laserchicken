import scipy.stats.stats as stats

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class PercentileFeatureExtractor(FeatureExtractor):
    """Height percentiles feature extractor class."""
    def __init__(self, percentile=50, data_key='z'):
        self.percentile = percentile
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return [self.generate_feature_name(self.percentile)]

    def generate_feature_name(self, percentile):
        return 'perc_{}_{}'.format(percentile, self.data_key)

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return [self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]

    def _extract_one(self, point_cloud, neighborhood):
        source_data = point_cloud[point][self.data_key]['data'][neighborhood]
        return stats.scoreatpercentile(source_data, self.percentile)

    def get_params(self):
        return ()
