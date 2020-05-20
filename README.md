Please cite the software if you are using it in your scientific publication.
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
- Python 3.5 or higher (3.6 is recommended)
- pip
```
pip install laserchicken
```

#### Necessary steps for making a new release
* Check citation.cff using general DOI for all version (option: create file via 'cffinit')
* Create .zenodo.json file from CITATION.cff (using cffconvert)  
```cffconvert --validate```  
```cffconvert --ignore-suspect-keys --outputformat zenodo --outfile .zenodo.json```
* Set new version number in laserchicken/_version.txt
* Check that documentation uses the correct version
* Edit Changelog (based on commits in https://github.com/eecolidar/laserchicken/compare/v0.3.2...master)
* Test if package can be installed with pip (`pip install .`)
* Create Github release
* Upload to pypi:  
```python setup.py sdist bdist_wheel```  
```python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*```  
(or ```python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*``` to test first)
* Check doi on zenodo


## Feature testing

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



