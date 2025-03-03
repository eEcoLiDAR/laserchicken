# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## Fixed

- compatibility issues with Numpy 2.0

## 0.6.1 - 2023-07-05

## Fixed
- select_polygon now works with shapely 2.0

## 0.6.0 - 2022-09-05
## Changed:
- continuous integration moved from travis to GH actions
- naming of band ratio's modified (symbol "<" dropped from label)

## Added
- releases published on PyPI using GH actions
- checklists included

## Fixed
- Fixed import of deprecated `scipy.stats.stats`

## 0.5.0 - 2022-05-20
## Changed:
- update documentation with table of features
- drop python 3.5 due to problematic lazperf dependency, includes CI on python 3.7 and 3.8
- drop usage of pylas (deprecated) in favour of laspy, with lazrs backend for LAZ compression

## Fixed
- minor fixes following updates in dateutils/click

## 0.4.2 - 2020-09-18
## Added:
- faster implementation of spatial selection

## Changed:
- all elements in WKT and shapefiles containing multiple polygons are considered (not only the first element)
- the validity conditions for multipolygons have been relaxed: valid adjacent polygons are now accepted

## Fixed:
- bug in copy_point_cloud with masks and zero-filled feature-arrays

## 0.4.1 - 2020-05-20
## Added:
- select_equal filter accepts list of values to compare to the points' attributes
- also the attribute-based filter functions optionally return a mask to allow filter combinations

## Fixed:
- bug in writing/reading 'None' as parameter in the PLY comments

## 0.4.0 - 2020-05-13
## Added:
- build_volume module
- the most relevant functions can be now imported directly from laserchicken
- reading/writing of binary PLY and LAZ files, with optional writing of selected attributes
- utility function to merge point-cloud data
- extra log tasks implemented: point-cloud log entries are introduced upon point-cloud loading, filtering, normalizing, merging and assigning to targets.
- select_polygon now supports multi-polygons and optionally return a mask for the selected points

## Changed:
- compute neighborhoods returns generator with neighborhoods instead of nested neighborhoods like it did before (breaking change!)
- Some of the existing modules have been renamed/restructured (breaking changes!):
    - `normalization` --> `normalize`
    - `feature_extraction` created (functions moved from `feature_extractor/__init__.py`)
    - `select` and `spatial_selection` merged into `filter`, with the function `select_polygon` allowing to deal with all the spatial selection functionalities
    - format-specific `read_*` and `write_*` modules replaced by `load` and `export`
- Dependency on `laspy` replaced by `pylas` + `lazperf` (easier reading/writing of LAS/LAZ files)

## 0.3.2 - 2019-12-12
## Added
- Features added:
    - max_intensity
    - min_intensity
    - range_intensity
    - mean_intensity
    - std_intensity
    - coeff_var_intensity

## Changed
- Features renamed:
    - max_norm_z --> min_normalized_height
    - min_norm_z --> max_normalized_height
    - range_norm_z --> range_normalized_height
    - mean_norm_z --> mean_normalized_height
    - std_norm_z --> std_normalized_height
    - coeff_var_norm_z --> coeff_var_normalized_height
    - density_absolute_mean_norm_z --> density_absolute_mean_normalized_height
    - entropy_norm_z --> entropy_normalized_height
    - kurto_norm_z --> kurto_normalized_height
    - skew_norm_z --> median_normalized_height
    - var_z --> skew_normalized_height
    - perc_1_norm_z --> var_normalized_height
    - perc_100_norm_z --> perc_1_normalized_height

## 0.3.1 - 2019-09-25
## Added
- Percentiles 1-100
- Percentiles normalized height 1-100
- Band ratio feature extractor
- Function to list available feature extractors
- Tutorial notebook

## Changed
- Echo ratio no longer gives percentage (removed factor 100)

## Fixed
- Bug in reading ply file with comments in unexpected format
- Bug in normal vector and slope

## Removed

## 0.3.0 - 2019-02-27
## Added
- Normalization module
- General tests that all current and future feature extractors will be checked against.
- Possibility to have a randomly subsampled (fixed) number of neighbors (eg for faster feature calculation)
- Added feature extractors based on normalized height

## Changed
- Many feature calculations are done in a vectorized way
- z_entropy feature renamed to entropy_z for consistency
- density_absolute_mean feature renamed to density_absolute_mean_z for consistency
- perc_10 features renamed to perc_10_z for consistency

## Fixed
- Corner cases for many feature extractors (e.g. zero points)
- Bug in slope feature calculation
- Bug in fix density absolute mean feature calculation

## Removed

## [0.1.0] - 2018-04-17
