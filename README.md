[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI Version](https://badge.fury.io/py/hydroeval.svg)](https://pypi.python.org/pypi/hydroeval)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2591217.svg)](https://doi.org/10.5281/zenodo.2591217)

# HydroEval - An efficient evaluator for streamflow time series in Python

`hydroeval` is an open-source `evaluator` of goodness of fit between simulated 
and observed streamflow time series in Python. It is licensed under GNU GPL-3.0 
(see [licence file](https://github.com/ThibHlln/hydroeval/blob/master/LICENCE.md) 
provided). The package provides a bundle of the most commonly used objective 
functions in hydrological science. The package is designed to calculate all 
objective functions in a vectorised manner (using [numpy](https://github.com/numpy/numpy), 
and therefore C code in the background) which makes for very efficient 
computation of the objective functions.

Please refer to the [online documentation](https://thibhlln.github.io/hydroeval) 
for further details and learn how to use the package. 

If you are using `hydroeval`, please consider citing the software as follows 
(click on the link to get the DOI of a specific version):
* Hallouin, T. (XXXX). HydroEval: Streamflow Simulations Evaluator (Version X.X.X). Zenodo. https://doi.org/10.5281/zenodo.2591217

## Version History

* 0.0.3 [09 Sep 2019]: [General enhancements](https://github.com/ThibHlln/hydroeval/releases/tag/v0.0.3)
* 0.0.2 [29 Nov 2018]: [General improvements](https://github.com/ThibHlln/hydroeval/releases/tag/v0.0.2)
* 0.0.1 [26 Oct 2018]: [First version of HydroEval](https://github.com/ThibHlln/hydroeval/releases/tag/v0.0.1)

## Acknowledgment

Early versions of this tool were developed with the financial support of 
Ireland's Environmental Protection Agency (Grant Number 2014-W-LS-5).
