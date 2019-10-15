<p align="left">
  <img src="https://raw.githubusercontent.com/eEcoLiDAR/laserchicken/master/laserchicken_logo.png" width="500"/>
</p>

[![Build Status](https://travis-ci.org/eEcoLiDAR/laserchicken.svg?branch=master)](https://travis-ci.org/eEcoLiDAR/laserchicken)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6e3836750fe14f34ba85e26956e8ef10)](https://www.codacy.com/app/c-meijer/eEcoLiDAR?utm_source=www.github.com&amp;utm_medium=referral&amp;utm_content=eEcoLiDAR/eEcoLiDAR&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/eEcoLiDAR/eEcoLiDAR/badge.svg)](https://coveralls.io/github/eEcoLiDAR/eEcoLiDAR)
[![DOI](https://zenodo.org/badge/95649056.svg)](https://zenodo.org/badge/latestdoi/95649056)
[![Documentation Status](https://readthedocs.org/projects/laserchicken/badge/?version=latest)](https://laserchicken.readthedocs.io/en/latest/)

Toolkit for handling point clouds created using airborne laser scanning (ALS). Find neighboring points in your point cloud and describe them as feature values. Read our [user manual](https://laserchicken.readthedocs.io/) and our (very modest) [tutorial](https://github.com/eEcoLiDAR/laserchicken/blob/master/tutorial.ipynb).

# Installation
Prerequisites:
- Python 3.5 or higher
- pip
```
pip install laserchicken
```

Included features:

 - band_ratio_1<normalized_height<2
 - band_ratio_2<normalized_height<3
 - band_ratio_3<normalized_height
 - band_ratio_normalized_height<1
 - coeff_var_norm_z
 - coeff_var_z
 - density_absolute_mean_norm_z
 - density_absolute_mean_z
 - echo_ratio
 - eigenv_1
 - eigenv_2
 - eigenv_3
 - entropy_norm_z
 - entropy_z
 - kurto_norm_z
 - kurto_z
 - max_norm_z
 - max_z
 - mean_norm_z
 - mean_z
 - median_norm_z
 - median_z
 - min_norm_z
 - min_z
 - normal_vector_1
 - normal_vector_2
 - normal_vector_3
 - perc_1_normalized_height until perc_100_normalized_height
 - perc_1_z until perc_100_z
 - point_density
 - pulse_penetration_ratio
 - range_norm_z
 - range_z
 - sigma_z
 - skew_norm_z
 - skew_z
 - slope
 - std_norm_z
 - std_z
 - var_norm_z
 - var_z'

**Feature testing**

All features were tested for the following general conditions:
- Output consistent point clouds and don't crash with artificial data, real data, all zero data (x, y or z), data without points, data with very low number of neighbors (0, 1, 2)
- Input should not be changed by the feature extractor

The specific features were tested as follows.

*Echo ratio*

A test was written with artificial data to check the correctness of the calculation with manually calculated ratio. Also tested on real data to make sure it doesn't crash, without checking for correctness. We could add a test for correctness with real data but we would need both that data and a verified ground truth.

*Eigenvalues*

Only sanity tests (l1>l2>l3) on real data and corner cases but no actual test for correctness. The code is very simple though and mainly calls numpy.linalg.eig.

*Height statistics (max_z','min_z','mean_z','median_z','std_z','var_z','coeff_var_z','skew_z','kurto_z)*

Tested on real data for correctness. It is however unclear where the ground truths come from. Code is mainly calling numpy methods that do all the work already. Only calculations in our code are:

```
range_z = max_z - min_z
coeff_var_z = np.std(z) / np.mean(z)
```
   
I don't know about any packages that could provide an out of the box coefficient of variance. This is probably because the calculation is so simple.

*Pulse penetration ratio*

Tested for correctness using artificial data against manually calculated values. No comparison was made with other implementations.

*Sigma_z*

Tested for correctness using artificial data against manually calculated values. No comparison was made with other implementations.

*Percentiles*

Tested for correctness using a simple case with artificial data against manually calculated values.

*point_density*

Tested for correctness on artificial data.



