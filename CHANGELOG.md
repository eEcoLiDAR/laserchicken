# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.1 - 2019-08-28
## Added
- Percentiles 1-100
- Percentiles normalized height 1-100
- Band ratio feature extractor 

## Changed
- Echo ratio no longer gives percentage (removed factor 100)
- Normalize method returns nothing as normalized height is added to the original point cloud already.

## Fixed
- Bug in reading ply file with comments in unexpected format
- Bug in normal vector and slope

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
