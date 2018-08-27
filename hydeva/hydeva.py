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
from scipy.stats import spearmanr


def evaluator(func, simulation_s, evaluation, axis=1, transform=None, epsilon=None):
    assert isinstance(simulation_s, np.ndarray)
    assert isinstance(evaluation, np.ndarray)
    assert (axis == 0) or (axis == 1)

    # check that the evaluation data provided is a single series of data
    if evaluation.ndim == 1:
        my_eval = evaluation[:]
    elif evaluation.ndim == 2:
        if (evaluation.shape[0] == 1) or (evaluation.shape[1] == 1):
            if evaluation.shape[1] > 1:
                my_eval = evaluation[0, :]
            elif evaluation.shape[0] > 1:
                my_eval = evaluation[:, 0]
            else:
                raise Exception('The evaluation 2D array does not contain enough data.')
        else:
            raise Exception('The evaluation 2D array does not feature a flat dimension.')
    else:
        raise Exception('The evaluation array contains more than 2 dimensions.')

    # transform the flow series if required
    if transform == 'log':  # log transformation
        if not epsilon:
            # determine an epsilon value to avoid log of zero (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, simulation_s = np.log(my_eval + epsilon), np.log(simulation_s + epsilon)
    elif transform == 'inv':  # inverse transformation
        if not epsilon:
            # determine an epsilon value to avoid zero divide (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(evaluation)
        my_eval, simulation_s = 1.0 / (my_eval + epsilon), 1.0 / (simulation_s + epsilon)
    elif transform == 'sqrt':  # square root transformation
        my_eval, simulation_s = np.sqrt(my_eval), np.sqrt(simulation_s)
    else:  # no transformation
        my_eval, simulation_s = my_eval, simulation_s

    # proceed according to the dimension of the simulation array (1D or 2D)
    if simulation_s.ndim == 1:
        if simulation_s.size == my_eval.size:
            # select subset of both series given the data availability in evaluation
            my_simu = simulation_s[~np.isnan(my_eval)]
            my_eval = my_eval[~np.isnan(my_eval)]
            return func(my_simu, my_eval)
        else:
            raise Exception('Simulation and evaluation arrays must be the same length.')
    elif simulation_s.ndim == 2:
        if simulation_s.shape[axis] == my_eval.size:  # check if lengths match (with default/user-defined axis)
            if axis == 1:
                if simulation_s.shape[0] > 1:
                    my_simu = simulation_s[:, ~np.isnan(my_eval)]
                    my_eval = my_eval[~np.isnan(my_eval)]
                    return np.apply_along_axis(func, axis, my_simu, my_eval)
                else:
                    my_simu = simulation_s[0, :][~np.isnan(my_eval)]
                    my_eval = my_eval[~np.isnan(my_eval)]
                    return func(my_simu, my_eval)
            else:  # axis == 0
                if simulation_s.shape[1] > 1:
                    my_simu = simulation_s[~np.isnan(my_eval), :]
                    my_eval = my_eval[~np.isnan(my_eval)]
                    return np.apply_along_axis(func, axis, my_simu, my_eval)
                else:
                    my_simu = simulation_s[:, 0][~np.isnan(my_eval)]
                    my_eval = my_eval[~np.isnan(my_eval)]
                    return func(my_simu, my_eval)
        else:
            raise Exception('Simulation and evaluation arrays must be the same length.')
    else:
        raise Exception('The simulation array contains more than 2 dimensions.')


def nse(simulation, evaluation):
    # calculate Nash-Sutcliffe Efficiency
    nse_ = 1 - (np.sum((evaluation - simulation) ** 2) /
                np.sum((evaluation - np.mean(evaluation)) ** 2))

    return nse_


def nse_c2m(simulation, evaluation):
    # calculate bounded formulation of NSE following C2M transformation after Mathevet et al. (2006)
    nse_ = nse(simulation, evaluation)
    nse_c2m_ = nse_ / (2 - nse_)

    return nse_c2m_


def kge(simulation, evaluation):
    # correlation coefficient (error in dynamics)
    cc = np.corrcoef(evaluation, simulation)[0, 1]
    # alpha (error in variability)
    alpha = np.std(simulation) / np.std(evaluation)
    # central tendency beta (error in volume)
    beta = np.sum(simulation) / np.sum(evaluation)
    # calculate Kling-Gupta Efficiency
    kge_ = 1 - np.sqrt((cc - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

    return kge_, cc, alpha, beta


def kge_c2m(simulation, evaluation):
    # calculate bounded formulation of KGE following C2M transformation after Mathevet et al. (2006)
    kge_ = kge(simulation, evaluation)[0]
    kge_c2m_ = kge_ / (2 - kge_)

    return kge_c2m_


def rmse(simulation, evaluation):
    # calculate root mean square error
    rmse_ = np.sqrt(np.mean((evaluation - simulation) ** 2))

    return rmse_


def spearman_rank_corr(simulation, evaluation):
    # return correlation only (rho)
    return spearmanr(simulation, evaluation)[0]


def mare(simulation, evaluation):
    # calculate mean absolute relative error (MARE)
    mare_ = np.sum(np.abs(evaluation - simulation)) / np.sum(evaluation)

    return mare_


def pbias(simulation, evaluation):
    # calculate percent bias
    pbias_ = 100 * np.sum(evaluation - simulation) / np.sum(evaluation)

    return pbias_
