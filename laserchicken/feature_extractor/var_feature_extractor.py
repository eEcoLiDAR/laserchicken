import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point


class VarianceFeatureExtractor(FeatureExtractor):
    """Calculates the variation on the z axis."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return ['var_' + self.data_key]

    def extract(self, source_point_cloud, neighborhood, targetpc, target_index, volume_description):
        if neighborhood:
            source_data = source_point_cloud[point][self.data_key]['data'][neighborhood]
            var_z = np.var(source_data)
        else:
            var_z = np.NaN
        return var_z
