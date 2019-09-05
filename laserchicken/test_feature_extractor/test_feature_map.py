"""Test that the map from feature names to extractor classes is correct."""
import unittest

from laserchicken import feature_extractor


class FeatureMapTests(unittest.TestCase):

    def test__feature_map(self):
        expected_features = ['point_density', 'echo_ratio', 'eigenv_1', 'eigenv_2', 'eigenv_3', 'normal_vector_1',
                             'normal_vector_2', 'normal_vector_3', 'slope', 'entropy_z', 'perc_10_z', 'perc_20_z',
                             'perc_30_z', 'perc_40_z', 'perc_50_z', 'perc_60_z', 'perc_70_z', 'perc_80_z', 'perc_90_z',
                             'perc_100_z', 'pulse_penetration_ratio', 'sigma_z', 'median_z', 'max_z', 'min_z',
                             'range_z', 'var_z', 'mean_z', 'std_z', 'coeff_var_z', 'skew_z', 'kurto_z', 'skew_norm_z',
                             'mean_norm_z', 'std_norm_z', 'coeff_var_norm_z', 'var_norm_z', 'max_norm_z', 'min_norm_z',
                             'range_norm_z', 'kurto_norm_z', 'entropy_norm_z', 'median_norm_z', 'perc_10_norm_z',
                             'perc_20_norm_z', 'perc_30_norm_z', 'perc_40_norm_z', 'perc_50_norm_z', 'perc_60_norm_z',
                             'perc_70_norm_z', 'perc_80_norm_z', 'perc_90_norm_z', 'perc_100_norm_z',
                             'density_absolute_mean_z', 'density_absolute_mean_norm_z']
        for feature in expected_features:
            self.assertIn(feature, feature_extractor.FEATURES)
