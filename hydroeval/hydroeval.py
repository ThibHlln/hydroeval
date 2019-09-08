# -*- coding: utf-8 -*-

# This file is part of HydroEval: An Evaluator for Stream Flow Time Series
# Copyright (C) 2019  Thibault Hallouin (1)
#
# (1) Dooge Centre for Water Resources Research, University College Dublin, Ireland
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


def evaluator(func, simulation_s, evaluation, axis=0, transform=None, epsilon=None):
    assert isinstance(simulation_s, np.ndarray)
    assert isinstance(evaluation, np.ndarray)
    assert (axis == 0) or (axis == 1)

    # check that the evaluation data provided is a single series of data
    if evaluation.ndim == 1:
        my_eval = np.reshape(evaluation, (evaluation.size, 1))
    elif evaluation.ndim == 2:
        if axis == 0:
            my_eval = evaluation
        else:
            my_eval = evaluation.T
    else:
        raise Exception('The evaluation array contains more than 2 dimensions.')
    if not my_eval.shape[1] == 1:
        raise Exception('The evaluation array does not contain a flat dimension.')

    # check the dimensions of the simulation data provided
    if simulation_s.ndim == 1:
        my_simu = np.reshape(simulation_s, (simulation_s.size, 1))
    elif simulation_s.ndim == 2:
        if axis == 0:
            my_simu = simulation_s
        else:
            my_simu = simulation_s.T
    else:
        raise Exception('The simulation array contains more than 2 dimensions.')

    # check that the two arrays have compatible lengths
    if not my_simu.shape[0] == my_eval.shape[0]:
        raise Exception('The simulation and evaluation arrays must have compatible dimensions.')

    # generate a subset of simulation and evaluation series where evaluation data is available
    my_simu = my_simu[~np.isnan(my_eval[:, 0]), :]
    my_eval = my_eval[~np.isnan(my_eval[:, 0]), :]

    # transform the flow series if required
    if transform == 'log':  # log transformation
        if not epsilon:
            # determine an epsilon value to avoid log of zero (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = np.log(my_eval + epsilon), np.log(my_simu + epsilon)
    elif transform == 'inv':  # inverse transformation
        if not epsilon:
            # determine an epsilon value to avoid zero divide (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = 1.0 / (my_eval + epsilon), 1.0 / (my_simu + epsilon)
    elif transform == 'sqrt':  # square root transformation
        my_eval, my_simu = np.sqrt(my_eval), np.sqrt(my_simu)

    # calculate the requested function and return in the same array orientation
    if axis == 0:
        return func(my_simu, my_eval)
    else:
        return func(my_simu, my_eval).T
