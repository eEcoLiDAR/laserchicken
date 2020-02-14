"""Test1 feature extractor."""
import numpy as np

from laserchicken import utils
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor


class Test1FeatureExtractor(FeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['test1_a', 'test1_b']

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return np.array([self._extract_one(target_point_cloud, target_index) for target_index in target_indices]).T

    def _extract_one(self, target_point_cloud, target_index):
        x, y, z = utils.get_point(target_point_cloud, target_index)
        return [0.5 * z, 1.5 * z]
