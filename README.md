[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# HydroEval - An open-source evaluator for stream flow time series in Python

HydroEval is an open-source evaluator of stream flow time series in Python. It is licensed under GNU GPL-3.0 (see [licence file](https://github.com/ThibHlln/hydroeval/blob/master/LICENCE.md) provided). The purpose of this evaluator is to compare observed and simulated hydrographs using one or more objective functions. HydroEval is designed to calculate all objective functions in a vectorised way which makes all computations very efficient using [numpy](https://github.com/numpy/numpy) (and hence C code under the hood).

## How to Install

The simplest way to install HydroEval is to use pip and a link to the GitHub repository:

	python -m pip install git+https://github.com/ThibHlln/hydroeval.git

Alternatively, you can download the source code (*i.e.* the GitHub repository) and, from the downloaded directory itself, run the command:

    python setup.py install
    
## Objective Functions

The objective functions currently available in HydroEval that evaluate the fit between observed and simulated stream flow timeseries are as follows:
* [Nash-Sutcliffe Efficiency](https://doi.org/10.1016/0022-1694(70)90255-6) (`nse`)
* [Original Kling-Gupta Efficiency](https://doi.org/10.1016/j.jhydrol.2009.08.003) (`kge`) and its three components (r, α, β)
* [Modified Kling-Gupta Efficiency](https://doi.org/10.1016/j.jhydrol.2012.01.011) (`kgeprime`) and its three components (r, γ, β)
* Root Mean Square Error (`rmse`)
* Mean Absolute Relative Error (`mare`)
* Percent Bias (`pbias`)

Moreover, KGE and NSE can be calculated in a bounded version following [Mathevet et al. (2008)](https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf):

* Bounded Nash-Sutcliffe Efficiency (`nse_c2m`)
* Bounded Original Kling-Gupta Efficiency (`kge_c2m`)
* Bounded Modified Kling-Gupta Efficiency (`kgeprime_c2m`)

Finally, any of the objective functions can take an optimal argument `transform`. This argument allows to apply a transformation on the observed and simulated stream flow timeseries prior the calculation of the objective function. The possible transformations are as follows:
* Inverted flows (using `transform='inv'`)
* Square Root-transformed flows (using `transform='sqrt'`)
* Natural Logarithm-transformed flows (using `transform='log'`)

## Dependencies

HydroEval requires the popular Python package `numpy` to be installed on the Python implementation where `hydroeval` is installed.

## Version History

* 0.0.1 [14 Oct 2018]: First version of HydroEval

## Acknowledgment

This tool was developed with the financial support of Ireland's Environmental Protection Agency (Grant Number 2014-W-LS-5).