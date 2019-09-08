[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI Version](https://badge.fury.io/py/hydroeval.svg)](https://pypi.python.org/pypi/hydroeval)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2591217.svg)](https://doi.org/10.5281/zenodo.2591217)

# HydroEval - An efficient evaluator for streamflow time series in Python

HydroEval is an open-source evaluator for streamflow time series in Python. It is licensed under GNU GPL-3.0 (see [licence file](https://github.com/ThibHlln/hydroeval/blob/master/LICENCE.md) provided). The purpose of this evaluator is to compare observed and simulated hydrographs using one or more objective functions. HydroEval is designed to calculate all objective functions in a vectorised manner (using [numpy](https://github.com/numpy/numpy), and therefore C code in the background) which makes for very efficient computation of the objective functions.

## How to Install

HydroEval is available on PyPI, so you can simply use pip and the name of the package:

    python -m pip install hydroeval

You can also use pip and a link to the GitHub repository directly:

	python -m pip install git+https://github.com/ThibHlln/hydroeval.git

Alternatively, you can download the source code (*i.e.* the GitHub repository) and, from the downloaded directory itself, run the command:

    python setup.py install

## How to Use

A tutorial in the form of a [Jupyter notebook](https://github.com/ThibHlln/hydroeval/blob/master/examples/api_usage_example.ipynb) is available to get started with the usage of HydroEval's API. The input files required for the tutorial are all provided in the `examples/` folder.

## How to Cite

If you are using HydroEval, please consider citing the software as follows (click on the link to get the DOI of a specific version):
* Hallouin, T. (XXXX). HydroEval: Streamflow Simulations Evaluator (Version X.X.X). Zenodo. https://doi.org/10.5281/zenodo.2591217

## Objective Functions Available

The objective functions currently available in HydroEval to evaluate the fit between observed and simulated stream flow time series are as follows:
* [Nash-Sutcliffe Efficiency](https://doi.org/10.1016/0022-1694(70)90255-6) (`nse`)
* [Original Kling-Gupta Efficiency](https://doi.org/10.1016/j.jhydrol.2009.08.003) (`kge`) and its three components (r, α, β)
* [Modified Kling-Gupta Efficiency](https://doi.org/10.1016/j.jhydrol.2012.01.011) (`kgeprime`) and its three components (r, γ, β)
* [Non-Parametric Kling-Gupta Efficiency](https://doi.org/10.1080/02626667.2018.1552002) (`kgenp`) and its three components (r, α, β)
* Root Mean Square Error (`rmse`)
* Mean Absolute Relative Error (`mare`)
* Percent Bias (`pbias`)

Moreover, KGE and NSE can be calculated in a bounded version following [Mathevet et al. (2006)](https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf):

* Bounded Nash-Sutcliffe Efficiency (`nse_c2m`)
* Bounded Original Kling-Gupta Efficiency (`kge_c2m`)
* Bounded Modified Kling-Gupta Efficiency (`kgeprime_c2m`)
* Bounded Non-Parametric Kling-Gupta Efficiency (`kgenp_c2m`)

Finally, any of the objective functions can take an optional argument `transform`. This argument allows to apply a transformation on both the observed and the simulated streamflow time series prior the calculation of the objective function. The possible transformations are as follows:
* Inverted flows (using `transform='inv'`)
* Square Root-transformed flows (using `transform='sqrt'`)
* Natural Logarithm-transformed flows (using `transform='log'`)

## Dependencies

HydroEval requires the Python package `numpy` to be installed on the Python interpreter where `hydroeval` is installed.

## Version History

* 0.0.3 [09 Sep 2019]: [General enhancements](https://github.com/ThibHlln/hydroeval/releases/tag/v0.0.3)
* 0.0.2 [29 Nov 2018]: [General improvements](https://github.com/ThibHlln/hydroeval/releases/tag/v0.0.2)
* 0.0.1 [26 Oct 2018]: [First version of HydroEval](https://github.com/ThibHlln/hydroeval/releases/tag/v0.0.1)

## Acknowledgment

This tool was developed with the financial support of Ireland's Environmental Protection Agency (Grant Number 2014-W-LS-5).
