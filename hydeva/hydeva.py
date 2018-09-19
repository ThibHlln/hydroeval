# -*- coding: utf-8 -*-

# This file is part of HYDEVA - For HYDrological EVAluations
# Copyright (C) 2018  Thibault Hallouin (1)
#
# (1) Dooge Centre for Water Resources Research, University College Dublin, Ireland
#
# HYDEVA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HYDEVA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HYDEVA. If not, see <http://www.gnu.org/licenses/>.

import numpy as np


def evaluator(func, simulation_s, evaluation, axis=1, transform=None, epsilon=None):
    assert isinstance(simulation_s, np.ndarray)
    assert isinstance(evaluation, np.ndarray)
    assert (axis == 0) or (axis == 1)

    # check that the evaluation data provided is a single series of data
    if evaluation.ndim == 1:
        my_eval = np.reshape(evaluation, (1, evaluation.size))
    elif evaluation.ndim == 2:
        if axis == 0:
            my_eval = evaluation.T
        else:
            my_eval = evaluation
    else:
        raise Exception('The evaluation array contains more than 2 dimensions.')
    if not my_eval.shape[0] == 1:
        raise Exception('The evaluation array does not contain a flat dimension.')

    # check the dimensions of the simulation data provided
    if simulation_s.ndim == 1:
        my_simu = np.reshape(simulation_s, (1, simulation_s.size))
    elif simulation_s.ndim == 2:
        if axis == 0:
            my_simu = simulation_s.T
        else:
            my_simu = simulation_s
    else:
        raise Exception('The simulation array contains more than 2 dimensions.')

    # check that the two arrays have compatible lengths
    if not my_simu.shape[1] == my_eval.shape[1]:
        raise Exception('The simulation and evaluation arrays must have compatible dimensions.')

    # generate a subset of simulation and evaluation series where evaluation data is available
    my_simu = my_simu[:, ~np.isnan(my_eval[0, :])]
    my_eval = my_eval[:, ~np.isnan(my_eval[0, :])]

    # transform the flow series if required
    if transform == 'log':  # log transformation
        if not epsilon:
            # determine an epsilon value to avoid log of zero (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = np.log(my_eval + epsilon), np.log(my_simu + epsilon)
    elif transform == 'inv':  # inverse transformation
        if not epsilon:
            # determine an epsilon value to avoid zero divide (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(evaluation)
        my_eval, my_simu = 1.0 / (my_eval + epsilon), 1.0 / (my_simu + epsilon)
    elif transform == 'sqrt':  # square root transformation
        my_eval, my_simu = np.sqrt(my_eval), np.sqrt(my_simu)

    # calculate the requested function
    return func(my_simu, my_eval)


def nse(simulation_s, evaluation):
    # calculate Nash-Sutcliffe Efficiency
    nse_ = 1 - (np.sum((evaluation - simulation_s) ** 2, axis=1, dtype=np.float64) /
                np.sum((evaluation - np.mean(evaluation)) ** 2))

    return nse_


def nse_c2m(simulation_s, evaluation):
    # calculate bounded formulation of NSE following C2M transformation after Mathevet et al. (2006)
    nse_ = nse(simulation_s, evaluation)
    nse_c2m_ = nse_ / (2 - nse_)

    return nse_c2m_


def kge(simulation_s, evaluation):
    # calculate correlation coefficient
    sim_mean = np.reshape(np.mean(simulation_s, axis=1), (simulation_s.shape[0], 1))
    obs_mean = np.mean(evaluation)
    r = np.sum((simulation_s - sim_mean) * (evaluation - obs_mean), axis=1, dtype=np.float64) / \
        np.sqrt(np.sum((simulation_s - sim_mean) ** 2, axis=1, dtype=np.float64) *
                np.sum((evaluation - obs_mean) ** 2, dtype=np.float64))
    # calculate alpha
    alpha = np.reshape(np.std(simulation_s, axis=1), (simulation_s.shape[0], 1)) / \
        np.std(evaluation)
    # calculate beta
    beta = np.reshape(np.sum(simulation_s, axis=1, dtype=np.float64), (simulation_s.shape[0], 1)) / \
        np.sum(evaluation, dtype=np.float64)
    # calculate the Kling-Gupta Efficiency KGE
    kge_ = 1 - np.sqrt(np.sum((np.reshape(r, (simulation_s.shape[0], 1)) - 1) ** 2 +
                              (alpha - 1) ** 2 + (beta - 1) ** 2, axis=1))

    return np.vstack((kge_, r, alpha[:, 0], beta[:, 0])).T


def kge_c2m(simulation_s, evaluation):
    # calculate bounded formulation of KGE following C2M transformation after Mathevet et al. (2006)
    kge_ = kge(simulation_s, evaluation)[0]
    kge_c2m_ = kge_ / (2 - kge_)

    return kge_c2m_


def kgeprime(simulation_s, evaluation):
    # calculate correlation coefficient
    sim_mean = np.reshape(np.mean(simulation_s, axis=1), (simulation_s.shape[0], 1))
    obs_mean = np.mean(evaluation)
    r = np.sum((simulation_s - sim_mean) * (evaluation - obs_mean), axis=1, dtype=np.float64) / \
        np.sqrt(np.sum((simulation_s - sim_mean) ** 2, axis=1, dtype=np.float64) *
                np.sum((evaluation - obs_mean) ** 2, dtype=np.float64))
    # calculate gamma
    gamma = (np.reshape(np.std(simulation_s, axis=1, dtype=np.float64), (simulation_s.shape[0], 1)) / sim_mean) / \
        (np.std(evaluation, dtype=np.float64) / obs_mean)
    # calculate beta
    beta = np.reshape(np.sum(simulation_s, axis=1, dtype=np.float64), (simulation_s.shape[0], 1)) / \
        np.sum(evaluation, dtype=np.float64)
    # calculate the modified Kling-Gupta Efficiency KGE'
    kge_ = 1 - np.sqrt(np.sum((np.reshape(r, (simulation_s.shape[0], 1)) - 1) ** 2 +
                              (gamma - 1) ** 2 + (beta - 1) ** 2, axis=1))

    return np.vstack((kge_, r, gamma[:, 0], beta[:, 0])).T


def kgeprime_c2m(simulation_s, evaluation):
    # calculate bounded formulation of KGE' following C2M transformation after Mathevet et al. (2006)
    kgeprime_ = kgeprime(simulation_s, evaluation)[0]
    kgeprime_c2m_ = kgeprime_ / (2 - kgeprime_)

    return kgeprime_c2m_


def rmse(simulation_s, evaluation):
    # calculate root mean square error
    rmse_ = np.sqrt(np.mean((evaluation - simulation_s) ** 2, axis=1, dtype=np.float64))

    return rmse_


def mare(simulation_s, evaluation):
    # calculate mean absolute relative error (MARE)
    mare_ = np.sum(np.abs(evaluation - simulation_s), axis=1, dtype=np.float64) / np.sum(evaluation)

    return mare_


def pbias(simulation_s, evaluation):
    # calculate percent bias
    pbias_ = 100 * np.sum(evaluation - simulation_s, axis=1, dtype=np.float64) / np.sum(evaluation)

    return pbias_
