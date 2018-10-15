[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# HydroEval - An open-source evaluator for stream flow time series in Python

HydroEval is an open-source evaluator of stream flow time series in Python. It is licensed under GNU GPL-3.0 (see [licence file](https://github.com/ThibHlln/hydroeval/blob/master/LICENCE.md) provided). HydroEval is designed to calculate all objective functions in a vectorised way which makes all computations very efficient using [numpy](https://github.com/numpy/numpy) (and hence C code under the hood).

## How to Install

The simplest way to install EFlowCalc is to use pip and a link to the GitHub repository:

	python -m pip install git+https://github.com/ThibHlln/hydroeval.git

Alternatively, you can download the source code (*i.e.* the GitHub repository) and, from the downloaded directory itself, run the command:

    python setup.py install

## Dependencies

HydroEval requires the popular Python packages `numpy` and `scipy` to be installed on the Python implementation where `hydroeval` is installed.

## Version History

* 0.0.1 [14 Oct 2018]: First version of HydroEval

## Acknowledgment

This tool was developed with the financial support of Ireland's Environmental Protection Agency (Grant Number 2014-W-LS-5).