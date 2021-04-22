An evaluator for streamflow time series in Python
-------------------------------------------------

.. image:: https://img.shields.io/pypi/v/hydroeval?color=blue
   :target: https://pypi.python.org/pypi/hydroeval
   :alt: PyPI Version
.. image:: https://zenodo.org/badge/145855846.svg
   :target: https://zenodo.org/badge/latestdoi/145855846
   :alt: DOI
.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: License: GPL v3
.. image:: https://img.shields.io/github/workflow/status/ThibHlln/hydroeval/Tests?label=tests
   :target: https://github.com/ThibHlln/hydroeval/actions/workflows/tests.yml
   :alt: GitHub Actions Test Workflow Status

`hydroeval` is an open-source `evaluator` of goodness of fit between
simulated and observed streamflow time series in Python. It is licensed
under GNU GPL-3.0. The package provides a bundle of the most commonly
used objective functions in hydrological science. The package is designed
to calculate all objective functions in a vectorised manner (using
`numpy <https://github.com/numpy/numpy>`_, and therefore C code
in the background) which makes for very efficient computation of the
objective functions.

If you are using `hydroeval`, please consider citing the software as
follows (click on the link to get the DOI of a specific version):

.. pull-quote::

   *Hallouin, T. (XXXX). HydroEval: Streamflow Simulations Evaluator (Version X.X.X). Zenodo.* `<https://doi.org/10.5281/zenodo.2591217>`_

.. rubric:: Brief overview of the API

.. code-block:: python

   import hydroeval as he

   simulations = [5.3, 4.2, 5.7, 2.3]
   evaluations = [4.7, 4.3, 5.5, 2.7]

   nse = he.evaluator(he.nse, simulations, evaluations)

   kge, r, alpha, beta = he.evaluator(he.kge, simulations, evaluations)


.. rubric:: Objective functions available

The objective functions currently available in `hydroeval` to evaluate the fit
between observed and simulated streamflow time series are as follows:

* `Nash-Sutcliffe Efficiency <https://doi.org/10.1016/0022-1694(70)90255-6>`_ (`nse`)
* `Original Kling-Gupta Efficiency <https://doi.org/10.1016/j.jhydrol.2009.08.003>`_ (`kge`) and its three components (r, α, β)
* `Modified Kling-Gupta Efficiency <https://doi.org/10.1016/j.jhydrol.2012.01.011>`_ (`kgeprime`) and its three components (r, γ, β)
* `Non-Parametric Kling-Gupta Efficiency <https://doi.org/10.1080/02626667.2018.1552002>`_ (`kgenp`) and its three components (r, α, β)
* Root Mean Square Error (`rmse`)
* Mean Absolute Relative Error (`mare`)
* Percent Bias (`pbias`)

Moreover, some objective functions can be calculated in a bounded version following
`Mathevet et al. (2006) <https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf>`_:

* Bounded Nash-Sutcliffe Efficiency (`nse_c2m`)
* Bounded Original Kling-Gupta Efficiency (`kge_c2m`)
* Bounded Modified Kling-Gupta Efficiency (`kgeprime_c2m`)
* Bounded Non-Parametric Kling-Gupta Efficiency (`kgenp_c2m`)

Finally, the `evaluator` can take an optional argument *transform*.
This argument allows to apply a transformation on both the observed and the
simulated streamflow time series prior the calculation of the objective function.
The possible transformations are as follows:

* Inverted flows (using `transform='inv'`)
* Square Root-transformed flows (using `transform='sqrt'`)
* Natural Logarithm-transformed flows (using `transform='log'`)

.. rubric:: Acknowledgement

Early versions of this tool were developed with the financial support of
Ireland's Environmental Protection Agency (Grant Number 2014-W-LS-5).
