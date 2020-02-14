"""Pulse penetration ratio and density absolute mean calculations.

See https://github.com/eEcoLiDAR/eEcoLiDAR/issues/23.
"""

import numpy as np

from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.keys import point, normalized_height

# classification according to
# http://www.asprs.org/wp-content/uploads/2010/12/LAS_1-4_R6.pdf
GROUND_TAGS = [2]


def _is_ground(i, point_cloud):
    return point_cloud[point]['raw_classification']["data"][i] in GROUND_TAGS


class DensityAbsoluteMeanFeatureExtractor(FeatureExtractor):
    """Feature extractor for the point density."""
    def __init__(self, data_key='z'):
        self.data_key = data_key

    @classmethod
    def requires(cls):
        return []

    def provides(self):
        return ['density_absolute_mean_' + self.data_key]

    def extract(self, point_cloud, neighborhoods, target_point_cloud, target_indices, volume_description):
        return [self._extract_one(point_cloud, neighborhood) for neighborhood in neighborhoods]

    def _extract_one(self, point_cloud, neighborhood):
        if 'raw_classification' not in point_cloud[point]:
            raise ValueError(
                'Missing raw_classification attribute which is necessary for calculating density_absolute_mean.')

        non_ground_indices = [i for i in neighborhood if not _is_ground(i, point_cloud)]
        density_absolute_mean_z = self._get_density_absolute_mean(non_ground_indices, point_cloud)

        return density_absolute_mean_z

    @staticmethod
    def _get_ground_indices(point_cloud, ground_tags):
        index_grd = []
        for ipt, c in enumerate(point_cloud):
            if c in ground_tags:
                index_grd.append(ipt)
        return index_grd

    def _get_density_absolute_mean(self, non_ground_indices, source_point_cloud):
        n_non_ground = len(non_ground_indices)
        data_non_ground = source_point_cloud[point][self.data_key]["data"][non_ground_indices]
        if n_non_ground == 0:
            density_absolute_mean = 0.
        else:
            density_absolute_mean = float(
                len(data_non_ground[data_non_ground > np.mean(data_non_ground)])) / n_non_ground * 100.
        return density_absolute_mean

    def get_params(self):
        return ()
