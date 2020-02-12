import unittest


class FromTutorial(unittest.TestCase):
    def test_tutorial_once(self):
        """This test should be identical to running all cells in the tutorial notebook once, in order."""
        from laserchicken.read_las import read
        point_cloud = read('testdata/AHN3.las')

        point_cloud

        from laserchicken.normalization import normalize
        normalize(point_cloud)

        point_cloud

        from laserchicken.spatial_selections import points_in_polygon_wkt
        polygon = "POLYGON(( 131963.984125 549718.375000," + \
                  " 132000.000125 549718.375000," + \
                  " 132000.000125 549797.063000," + \
                  " 131963.984125 549797.063000," + \
                  " 131963.984125 549718.375000))"
        points_in_area = points_in_polygon_wkt(point_cloud, polygon)
        point_cloud = points_in_area

        from laserchicken.select import select_above, select_below
        points_below_1_meter = select_below(point_cloud, 'normalized_height', 1)
        points_above_1_meter = select_above(point_cloud, 'normalized_height', 1)

        from laserchicken.compute_neighbors import compute_neighborhoods
        from laserchicken.volume_specification import Sphere
        targets = point_cloud
        volume = Sphere(5)
        neighbors = compute_neighborhoods(point_cloud, targets, volume)

        from laserchicken.feature_extractor import compute_features
        compute_features(point_cloud, neighbors, targets, ['std_z', 'mean_z', 'slope'], volume)

        from laserchicken.feature_extractor import register_new_feature_extractor
        from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
        register_new_feature_extractor(BandRatioFeatureExtractor(None, 1, data_key='normalized_height'))
        register_new_feature_extractor(BandRatioFeatureExtractor(1, 2, data_key='normalized_height'))
        register_new_feature_extractor(BandRatioFeatureExtractor(2, None, data_key='normalized_height'))
        register_new_feature_extractor(BandRatioFeatureExtractor(None, 0, data_key='z'))

        from laserchicken.feature_extractor import list_feature_names
        sorted(list_feature_names())

        from laserchicken.volume_specification import InfiniteCylinder
        cylinder = InfiniteCylinder(5)
        neighborhoods = compute_neighborhoods(point_cloud, targets, cylinder)
        compute_features(point_cloud, neighborhoods, targets, ['band_ratio_1<normalized_height<2'], cylinder)

        from laserchicken.write_ply import write
        write(point_cloud, 'my_output.ply')