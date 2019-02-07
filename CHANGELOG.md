# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Normalization module
- General tests that all current and future feature extractors will be checked against.
- Possibility to have a randomly subsampled (fixed) number of neighbors (eg for faster feature calculation) 

## Changed
- Many feature calculations are done in a vectorized way

## Fixed
- Corner cases for many feature extractors (e.g. zero points)

## Removed

## [0.1.0] - 2018-04-17
