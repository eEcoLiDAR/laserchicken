.. Laserchicken documentation master file, created by
   sphinx-quickstart on Thu Oct  3 15:28:52 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Laserchicken's documentation!
========================================
Laserchicken is a user-extendable, cross-platform Python tool for
extracting statistical properties (features in machine learning jargon)
of flexibly defined subsets of point cloud data.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

User manual
===========

Laserchicken processes point clouds from Airborne Laser Scanning in LAS/LAZ format, and normalizes, and filters the points, finds neighbors for targeted points and calculates features.

.. image:: figures/workflow.png
  :alt: Laserchicken workflow

The figure shows the default workflow for which Laserchicken was intended. In short, a point cloud is loaded from a LAS or LAZ or PLY file. After this, points can be filtered by various criteria, and the height can be normalized. A point cloud of targets are loaded. See below a description of what is the concept of a target point. For every target point, neighbors will be computed. Based on the list of neighbors, features are extracted that effectively describe the neighborhood of each target point.

Environment and target point cloud
==================================

In Laserchicken, the LiDAR dataset is referred to as the environment point cloud (EPC), and the subsets of points over which a metric is to be calculated are referred to as neighborhoods. Each neighborhood is defined by a target volume and a target point (e.g. a cube of a certain size and its centroid, respectively), with all points enclosed in the volume constituting the neighborhood.

See below an illustration of a target point cloud (green points) representing the centroids of a regular grid cell, and the neighborhoods (red points) defined by a square infinite cell target volume (red columns). Features are calculated over the neighborhood of each target point and then associated with the target point, thus forming the enriched target point cloud (eTPC). Points that are not included in the neighborhoods are shown in in black.

.. image:: figures/targets.png
  :width: 450
  :alt: targets and environment point cloud

Four volume definitions are implemented: an infinite square cell, an infinite cylinder, a cube and a sphere.

.. image:: figures/cell.png
  :width: 300
  :alt: cell
.. image:: figures/cylinder.png
  :width: 300
  :alt: cylinder
.. image:: figures/sphere.png
  :width: 300
  :alt: sphere
.. image:: figures/voxel.png
  :width: 300
  :alt: voxel

All target points together form the target point cloud (TPC). The TPC can be freely defined by the user, and can be for instance identical to the environment point cloud or alternatively a regular grid as illustrated above.
Features are calculated over the list of neighborhoods, with the feature values being associated with each neighborhood's defining target point, thus forming the enriched target point cloud (eTPC).

Modules
=======

Each module from the workflow is described below and an example of its usage is given. If you need more examples, be sure to have a look of the unit tests in the Laserchicken's source code.

Load
----

The load module provides functionality to load  point cloud datasets provided in ASPRS LAS/LAZ, or in PLY format, and is used for both input point clouds. In conjunction with
the PDAL library (https://pdal.io/), this provides access to a comprehensive range of point cloud data formats.

Example from the tutorial notebook::

   from laserchicken.read_las import read
   point_cloud = read('testdata/AHN3.las')

Normalize
---------

A number of features (Table~\ref{tab_features}) require the normalized height above ground as input. Laserchicken provides the option of internally constructing a digital terrain model (DTM) and deriving this quantity. To this end, the EPC is divided into small cells 1m or 2.5m squared). The lowest point in each cell is taken as the height of the DTM. Each point in the cell is then assigned a normalized height with respect to the derived DTM height. This results in strictly positive heights and smooths variations in elevation on scales larger than the cell size. The normalized EPC can be used directly in further analysis, or serialized to disk.

Example from the tutorial notebook::

   from laserchicken.normalization import normalize
   normalize(point_cloud)

Filter
------
Laserchicken provides the option of filtering the EPC prior to extracting features. Points may be filtered on the value of a single attribute relative to a specified threshold (e.g. above a certain normalized height above ground), or on specific values of their attributes (e.g. LAS standard classification). It is also possible to filter with (geo-)spatial layers such as polygons (e.g. regions of interest, land cover types), i.e. selectively including or excluding points.

Example of spatial filtering from the tutorial notebook::

   from laserchicken.spatial_selections import points_in_polygon_wkt
   polygon = "POLYGON(( 131963.984125 549718.375000," + \
                      " 132000.000125 549718.375000," + \
                      " 132000.000125 549797.063000," + \
                      " 131963.984125 549797.063000," + \
                      " 131963.984125 549718.375000))"
   points_in_area = points_in_polygon_wkt(point_cloud, polygon)
   point_cloud = points_in_area

Example of applying a filter on the theshold of an attribute::

   from laserchicken.select import select_above, select_below
   points_below_1_meter = select_below(point_cloud, 'normalized_height', 1)
   points_above_1_meter = select_above(point_cloud, 'normalized_height', 1)


Compute neighbors
-----------------

The Compute neighbors module constructs the neighborhoods as defined by the TPC
and target volume by identifying the points in the EPC which reside in the specified volume
centered on the target points, returning each as a list of indices to the EPC. This essential step of computing neighboring points for large samples of points is computationally expensive. Laserchicken uses the optimized ckDtree class (kdTrees are a space-partitioning data structure) provided by the scipy library to organize both the EPC
and TPC in kdTrees in an initial step prior to the computation of neighbors, subsequently accelerating the process of computing neighbors by using the indices of the points with respect to the kDtrees.

Example from the tutorial notebook::

   from laserchicken.compute_neighbors import compute_neighborhoods
   from laserchicken.volume_specification import Sphere
   targets = point_cloud
   volume = Sphere(5)
   neighbors = compute_neighborhoods(point_cloud, targets, volume)

Note that in the above example, neighbors is a generator and can only be iterated once. If you would want to do multiple calculations without recalculating the neighbors, you can copy the neighbors to a list. This is not done by default because neighbors can quickly grow quite large so that available RAM unnecessarily becomes the bottle neck.

Features
--------

Feature extraction requires the EPC, the TPC, the computed list of neighborhoods, and a list of requested features as input. For each target point it selects the points of the associated neighborhood and calculates a vector of the requested features over these. This feature vector is appended to the target point, thus defining the eTPC.

Currently, a number of features are implemented, including percentiles of the height distribution and eigenvectors. Computationally expensive calculations requiring multi-dimensional linear algebraic operations (e.g. eigenvectors and eigenvalues) have been vectorized using the einsum function of the numpy library to optimize performance. Their implementation can serve as a
template for new features requiring similar operations.

Example from the tutorial notebook::

   from laserchicken.feature_extractor import compute_features
   for x in neighbors:
       compute_features(point_cloud, x, 0, targets, ['std_z','mean_z','slope'], volume)

Features can be parameterized. If you need different parameters for them then their defaults you need to register them with these prior to using them.

Example of adding a few parameterized band ratio features on different attributes::

   from laserchicken.feature_extractor import register_new_feature_extractor
   from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
   register_new_feature_extractor(BandRatioFeatureExtractor(None,1,data_key='normalized_height'))
   register_new_feature_extractor(BandRatioFeatureExtractor(1,2,data_key='normalized_height'))
   register_new_feature_extractor(BandRatioFeatureExtractor(2,None,data_key='normalized_height'))
   register_new_feature_extractor(BandRatioFeatureExtractor(None,0,data_key='z'))

The currently registered features can be listed as followes::

   from laserchicken.feature_extractor import list_feature_names
   sorted(list_feature_names())

Which outputs something like::

   ['band_ratio_1<normalized_height<2',
    'band_ratio_2<normalized_height',
    'band_ratio_2<normalized_height<3',
    'band_ratio_3<normalized_height',
    'band_ratio_normalized_height<1',
    'band_ratio_z<0',
    'coeff_var_norm_z',
    'coeff_var_z',
    'density_absolute_mean_norm_z',
    'density_absolute_mean_z',
    'echo_ratio',
    'eigenv_1',
    'eigenv_2',
    'eigenv_3',
    'entropy_norm_z',
    'entropy_z',
    'kurto_norm_z',
    'kurto_z',
    'max_norm_z',
    'max_z',
    'mean_norm_z',
    'mean_z',
    'median_norm_z',
    'median_z',
    'min_norm_z',
    'min_z',
    'normal_vector_1',
    'normal_vector_2',
    'normal_vector_3',
    'perc_100_normalized_height',
    'perc_100_z',
    'perc_10_normalized_height',
    'perc_10_z',
    ...
    'perc_99_normalized_height',
    'perc_99_z',
    'perc_9_normalized_height',
    'perc_9_z',
    'point_density',
    'pulse_penetration_ratio',
    'range_norm_z',
    'range_z',
    'sigma_z',
    'skew_norm_z',
    'skew_z',
    'slope',
    'std_norm_z',
    'std_z',
    'var_norm_z',
    'var_z']

Export
------

Laserchicken can write to PLY, CSV, or LAS/LAZ format for further analysis with the user's choice of software. The PLY format is preferred, as it is flexibly extendable and is the only format Laserchicken will write provenance data to. It is also a widely supported point cloud format.

Example from the tutorial notebook::

   from laserchicken.write_ply import write
   write(point_cloud, 'my_output.ply')


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
