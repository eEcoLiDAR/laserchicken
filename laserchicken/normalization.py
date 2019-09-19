from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken import keys
from laserchicken.feature_extractor.range_z_feature_extractor import RangeZFeatureExtractor as range_extractor
import numpy as np

from laserchicken.test_tools import create_point_cloud
from laserchicken.utils import add_metadata
from laserchicken.volume_specification import Cell


def normalize(point_cloud, cell_size=None):
    """Calculate normalized height for every point and add this to the given point cloud (in place).

    A simple digital terrain model (DTM) is calculated by taking the minimum of every cell. If no cell size is given,
    the global minimum of the point cloud is used. The minimum is interpreted as DTM. The normalized height is
    calculated by subtracting the DTM from the z value for every point.

    :param point_cloud input point cloud that will be enriched with a normalized height attribute
    :param cell_size:
    """
    z = point_cloud[keys.point]['z']['data']
    point_cloud[keys.point][keys.normalized_height] = {"type": 'float64', "data": np.zeros_like(z)}
    if cell_size is None:
        _add_normalized_height_by_global_minimum(point_cloud, z)
    else:
        _add_normalized_height_by_cell_minimum(cell_size, point_cloud, z)
    import sys
    module = sys.modules[__name__]
    add_metadata(point_cloud, module, {'cell_size': cell_size})


def _add_normalized_height_by_cell_minimum(cell_size, point_cloud, z):
    targets = _create_spanning_grid(point_cloud, cell_size)
    neighborhood_sets = compute_neighborhoods(point_cloud, targets, Cell(cell_size), sample_size=None)
    for neighborhood_set in neighborhood_sets:
        for neighborhood in neighborhood_set:
            _, min_z, _ = range_extractor().extract(point_cloud, neighborhood, None, None, None)
            point_cloud[keys.point][keys.normalized_height]['data'][neighborhood] = z[neighborhood] - min_z


def _add_normalized_height_by_global_minimum(point_cloud, z):
    n_points = point_cloud[keys.point][keys.normalized_height]['data'].size
    _, min_z, _ = range_extractor().extract(point_cloud, range(n_points), None, None, None)
    point_cloud[keys.point][keys.normalized_height]['data'] = z - min_z


def _create_spanning_grid(point_cloud, cell_size):
    x = point_cloud[keys.point]['x']['data']
    y = point_cloud[keys.point]['y']['data']
    min_x = np.min(x)
    max_x = np.max(x)
    min_y = np.min(y)
    max_y = np.max(y)

    cell_x_lengths, n_grid_points = _count_steps_and_points(cell_size, max_x, max_y, min_x, min_y)

    xs = [min_x + cell_size * (0.5 + (i % cell_x_lengths)) for i in range(n_grid_points)]
    ys = [min_y + cell_size * (0.5 + np.floor(i / cell_x_lengths)) for i in range(n_grid_points)]
    zs = np.zeros_like(xs)
    return create_point_cloud(xs, ys, zs)


def _count_steps_and_points(cell_size, max_x, max_y, min_x, min_y):
    cell_x_lengths = _count_steps(min_x, max_x, cell_size)
    cell_y_lengths = _count_steps(min_y, max_y, cell_size)
    n_grid_points = cell_x_lengths * cell_y_lengths
    return cell_x_lengths, n_grid_points


def _count_steps(min_x, max_x, cell_size):
    """Count the number of steps in a grid in a single direction."""
    return max(int(np.ceil((max_x - min_x) / float(cell_size))), 1)
