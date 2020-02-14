# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.3 - 2020-
## Added:
- build_volume module
- the most relevant functions can be now imported directly from laserchicken

## Changed:
- compute neighborhoods returns generator with neighborhoods instead of nested neighborhoods like it did before (breaking change!)
- Some of the existing modules have been renamed/restructured (breaking changes!):
    - `normalization` --> `normalize`
    - `feature_extraction` created (functions moved from `feature_extractor/__init__.py`)
    - `select` and `spatial_selection` merged into `filter`, with the function `select_polygon` allowing to deal with all the spatial selection functionalities
    - format-specific `read_*` and `write_*` modules replaced by `load` and `export`

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
