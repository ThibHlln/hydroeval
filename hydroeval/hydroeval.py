# This file is part of HydroEval: an evaluator for streamflow time series
# Copyright (C) 2020  Thibault Hallouin
#
# HydroEval is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HydroEval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HydroEval. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import numbers


def evaluator(obj_fn, simulations, evaluation, axis=0,
              transform=None, epsilon=None):
    """Evaluate the goodness of fit between one time series of simulated
    streamflow stored in a 1D array (or several time series of equal
    length stored in a 2D array) and one time series of the corresponding
    observed streamflow for the same period stored in a 1D array. Missing
    values can be set as `numpy.nan` for paiwise deletion to be performed.

    :Parameters:

        obj_fn: `hydroeval` objective function
            The objective function to use to evaluate the goodness of
            fit between the *simulations* series and the *evaluation*
            series.

            *Parameter example:* ::

                obj_fn=hydroeval.nse

            *Parameter example:* ::

                obj_fn=hydroeval.kge

        simulations: array-like object
            The array of simulated streamflow values to be compared
            against the *observation* using the *obj_fn*. Note, the
            array can be one or two dimensional. If it is 2D, the time
            dimension must be the one specified through *axis*.

        evaluation: array-like object
            The array of observed streamflow values to be compared
            against the *simulations* using the *obj_fn*. Note, the
            array can be one or two dimensional. If it is 2D, the
            dimension specified through *axis* must be of size 1.
            Moreover, the length of the *evaluation* series must match
            the length of *simulations* series ― missing values must
            be set as `numpy.nan` so that pairwise deletion in both
            *simulations* and *evaluation* series can be performed prior
            the calculation of the *obj_fn*.

        axis: `int`, optional
            The axis along which the *simulations* and/or *evaluation*
            time dimension is, if any is a 2D array. If not provided,
            set to default value 0.

        transform: `str`, optional
            The transformation to apply to both the *simulations* and
            *evaluation* streamflow values **Q** prior the evaluation of
            the goodness of fit with the *obj_fn*. If not provided, set
            to default value `None` (i.e. no transformation). The
            supported transform arguments are listed in the table below.

            =========================  =================================
            transformations            details
            =========================  =================================
            ``'inv'``                  The reciprocal function
                                       **f(Q) = 1/Q** is applied.
            ``'sqrt'``                 The square root function
                                       **f(Q) = √Q** is applied.
            ``'log'``                  The natural logarithm function
                                       **f(Q) = ln(Q)** is applied.
            =========================  =================================

        epsilon: `float`, optional
            The value of the small constant ε to add to both the
            *simulations* and *evaluation* streamflow values **Q** prior
            the evaluation of the goodness of fit with the *obj_fn*
            when the *transform* is the reciprocal function or the
            natural logarithm since neither are defined for 0. If not
            provided, set to default value equal to one hundredth of
            the mean of the *evaluation* streamflow series, as
            recommended by `Pushpalatha et al. (2012)
            <https://doi.org/10.1016/j.jhydrol.2011.11.055>`_.

    **Examples**

    >>> import hydroeval as he
    >>> print(he.evaluator(he.nse, [5.3, 4.2, 5.7, 2.3], [4.7, 4.3, 5.5, 2.7]))
    [0.86298077]
    >>> print(he.evaluator(he.kge, [5.3, 4.2, 5.7, 2.3], [4.7, 4.3, 5.5, 2.7]))
    [[0.7066232 ]
     [0.98213905]
     [1.2923127 ]
     [1.01744186]]

    Computations on multiple simulation series at once are possible.

    >>> print(he.evaluator(he.kge, [[5.3, 4.6], [4.2, 4.2], [5.7, 5.3], [2.3, 2.8]],
    ...                    [4.7, 4.3, 5.5, 2.7]))
    [[0.7066232  0.8929297 ]
     [0.98213905 0.99985551]
     [1.2923127  0.89436   ]
     [1.01744186 0.98255814]]
    >>> print(he.evaluator(he.kge, [[5.3, 4.2, 5.7, 2.3], [4.6, 4.2, 5.3, 2.8]],
    ...                    [4.7, 4.3, 5.5, 2.7], axis=1))
    [[0.7066232  0.98213905 1.2923127  1.01744186]
     [0.8929297  0.99985551 0.89436    0.98255814]]

    In case of missing observations (flagged as NaN), `hydroeval` performs pairwise deletion.

    >>> import numpy as np
    >>> print(he.evaluator(he.nse,
    ...                    [5.3, 4.2, 5.7, 2.3], [4.7, 4.3, np.nan, 2.7]))
    [0.76339286]
    >>> print(he.evaluator(he.nse,
    ...                    [5.3, 4.2, 2.3], [4.7, 4.3, 2.7]))
    [0.76339286]

    Pre-computation transformations on data are possible with parameter *transform*.

    >>> print(he.evaluator(he.nse, [5.3, 4.2, 5.7, 2.3], [4.7, 4.3, 5.5, 2.7],
    ...                    transform='sqrt'))
    [0.86356266]

    When using reciprocal or logarithm transform function, default *epsilon*
    added to all flows to avoid zero flows. *epsilon* is customisable.

    >>> print(he.evaluator(he.kge, [5.3, 4.2, 5.7, 0.0], [4.7, 4.3, 5.5, 0.1],
    ...                    transform='inv'))
    [[-2.78380731]
     [ 0.99999157]
     [ 3.82066207]
     [ 3.52211483]]
    >>> print(he.evaluator(he.kge, [5.3, 4.2, 5.7, 0.0], [4.7, 4.3, 5.5, 0.1],
    ...                    transform='inv', epsilon=0.073))
    [[-0.88255825]
     [ 0.99999145]
     [ 2.42185928]
     [ 2.23383214]]

    """
    # check types/values of the different arguments given,
    # if not compliant, abort
    simulations = np.asarray(simulations)
    if not simulations.shape:
        raise TypeError('simulations must be an array')
    if not np.issubdtype(simulations.dtype, np.number):
        raise TypeError('simulations array must contain numerical values')
    evaluation = np.asarray(evaluation)
    if not evaluation.shape:
        raise TypeError('evaluation must be an array')
    if not np.issubdtype(evaluation.dtype, np.number):
        raise TypeError('evaluation array must contain numerical values')
    if axis not in (0, 1):
        raise IndexError('index for axis must be 0 or 1')
    if transform is not None:
        if transform not in ('inv', 'sqrt', 'log'):
            raise ValueError('transform parameter not supported')
    if epsilon is not None:
        if not isinstance(epsilon, numbers.Number):
            raise TypeError('epsilon must be a number')

    # check that the evaluation data provided is a single series of data
    if evaluation.ndim == 1:
        my_eval = np.reshape(evaluation, (evaluation.size, 1))
    elif evaluation.ndim == 2:
        if axis == 0:
            my_eval = evaluation
        else:  # axis == 1
            my_eval = evaluation.T
    else:
        raise ValueError('evaluation array contains more than 2 dimensions')
    if not my_eval.shape[1] == 1:
        raise ValueError('evaluation array is not flat')

    # check the dimensions of the simulation data provided
    if simulations.ndim == 1:
        my_simu = np.reshape(simulations, (simulations.size, 1))
    elif simulations.ndim == 2:
        if axis == 0:
            my_simu = simulations
        else:  # axis == 1
            my_simu = simulations.T
    else:
        raise ValueError('simulation array contains more than 2 dimensions')

    # check that the two arrays have compatible lengths
    if not my_simu.shape[0] == my_eval.shape[0]:
        raise ValueError('simulation and evaluation arrays feature '
                         'incompatible dimensions')

    # generate a subset of simulation and evaluation series
    # where evaluation data is available
    my_simu = my_simu[~np.isnan(my_eval[:, 0]), :]
    my_eval = my_eval[~np.isnan(my_eval[:, 0]), :]

    # transform the flow series if required
    if transform == 'log':  # log transformation
        if not epsilon:
            # determine an epsilon value to avoid log of zero
            # (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = np.log(my_eval + epsilon), np.log(my_simu + epsilon)
    elif transform == 'inv':  # inverse transformation
        if not epsilon:
            # determine an epsilon value to avoid zero divide
            # (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = 1.0 / (my_eval + epsilon), 1.0 / (my_simu + epsilon)
    elif transform == 'sqrt':  # square root transformation
        my_eval, my_simu = np.sqrt(my_eval), np.sqrt(my_simu)

    # calculate the requested function and return in the same array orientation
    if axis == 0:
        return obj_fn(my_simu, my_eval)
    else:
        return obj_fn(my_simu, my_eval).T
