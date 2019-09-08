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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OBJECTIVE FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Nash-Sutcliffe Efficiency (Nash and Sutcliffe 1970 - https://doi.org/10.1016/0022-1694(70)90255-6)
def nse(simulation_s, evaluation):
    nse_ = 1 - (np.sum((evaluation - simulation_s) ** 2, axis=0, dtype=np.float64) /
                np.sum((evaluation - np.mean(evaluation)) ** 2, dtype=np.float64))

    return nse_


# Original Kling-Gupta Efficiency (Gupta et al. 2009 - https://doi.org/10.1016/j.jhydrol.2009.08.003)
def kge(simulation_s, evaluation):
    # calculate error in timing and dynamics r (Pearson's correlation coefficient)
    sim_mean = np.mean(simulation_s, axis=0, dtype=np.float64)
    obs_mean = np.mean(evaluation, dtype=np.float64)
    r = np.sum((simulation_s - sim_mean) * (evaluation - obs_mean), axis=0, dtype=np.float64) / \
        np.sqrt(np.sum((simulation_s - sim_mean) ** 2, axis=0, dtype=np.float64) *
                np.sum((evaluation - obs_mean) ** 2, dtype=np.float64))
    # calculate error in spread of flow alpha
    alpha = np.std(simulation_s, axis=0) / np.std(evaluation, dtype=np.float64)
    # calculate error in volume beta (bias of mean discharge)
    beta = np.sum(simulation_s, axis=0, dtype=np.float64) / np.sum(evaluation, dtype=np.float64)
    # calculate the Kling-Gupta Efficiency KGE
    kge_ = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

    return np.vstack((kge_, r, alpha, beta))


# Modified Kling-Gupta Efficiency (Kling et al. 2012 - https://doi.org/10.1016/j.jhydrol.2012.01.011)
def kgeprime(simulation_s, evaluation):
    # calculate error in timing and dynamics r (Pearson's correlation coefficient)
    sim_mean = np.mean(simulation_s, axis=0, dtype=np.float64)
    obs_mean = np.mean(evaluation, dtype=np.float64)
    r = np.sum((simulation_s - sim_mean) * (evaluation - obs_mean), axis=0, dtype=np.float64) / \
        np.sqrt(np.sum((simulation_s - sim_mean) ** 2, axis=0, dtype=np.float64) *
                np.sum((evaluation - obs_mean) ** 2, dtype=np.float64))
    # calculate error in spread of flow gamma (avoiding cross correlation with bias by dividing by the mean)
    gamma = (np.std(simulation_s, axis=0, dtype=np.float64) / sim_mean) / \
        (np.std(evaluation, dtype=np.float64) / obs_mean)
    # calculate error in volume beta (bias of mean discharge)
    beta = np.mean(simulation_s, axis=0, dtype=np.float64) / np.mean(evaluation, axis=0, dtype=np.float64)
    # calculate the modified Kling-Gupta Efficiency KGE'
    kgeprime_ = 1 - np.sqrt((r - 1) ** 2 + (gamma - 1) ** 2 + (beta - 1) ** 2)

    return np.vstack((kgeprime_, r, gamma, beta))


# Non-Parametric Kling-Gupta Efficiency (Pool et al. 2018 - https://doi.org/10.1080/02626667.2018.1552002)
def kgenp(simulation_s, evaluation):
    # calculate error in timing and dynamics r (Spearman's correlation coefficient)
    sim_rank = np.argsort(np.argsort(simulation_s, axis=0), axis=0)
    obs_rank = np.argsort(np.argsort(evaluation, axis=0), axis=0)
    r = np.sum((obs_rank - np.mean(obs_rank, axis=0, dtype=np.float64)) *
               (sim_rank - np.mean(sim_rank, axis=0, dtype=np.float64)), axis=0) / \
        np.sqrt(np.sum((obs_rank - np.mean(obs_rank, axis=0, dtype=np.float64)) ** 2, axis=0) *
                (np.sum((sim_rank - np.mean(sim_rank, axis=0, dtype=np.float64)) ** 2, axis=0)))
    # calculate error in timing and dynamics alpha (flow duration curve)
    sim_fdc = np.sort(simulation_s / (simulation_s.shape[0] * np.mean(simulation_s, axis=0, dtype=np.float64)), axis=0)
    obs_fdc = np.sort(evaluation / (evaluation.shape[0] * np.mean(evaluation, axis=0, dtype=np.float64)), axis=0)
    alpha = 1 - 0.5 * np.sum(np.abs(sim_fdc - obs_fdc), axis=0)
    # calculate error in volume beta (bias of mean discharge)
    beta = np.mean(simulation_s, axis=0) / np.mean(evaluation, axis=0, dtype=np.float64)
    # calculate the non-parametric Kling-Gupta Efficiency KGEnp
    kgenp_ = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

    return np.vstack((kgenp_, r, alpha, beta))


# Root Mean Square Error
def rmse(simulation_s, evaluation):
    rmse_ = np.sqrt(np.mean((evaluation - simulation_s) ** 2, axis=0, dtype=np.float64))

    return rmse_


# Mean Absolute Relative Error
def mare(simulation_s, evaluation):
    mare_ = np.sum(np.abs(evaluation - simulation_s), axis=0, dtype=np.float64) / np.sum(evaluation)

    return mare_


# Percent Bias
def pbias(simulation_s, evaluation):
    pbias_ = 100 * np.sum(evaluation - simulation_s, axis=0, dtype=np.float64) / np.sum(evaluation)

    return pbias_

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BOUNDED VERSIONS OF SOME OBJECTIVE FUNCTIONS
# (After Mathevet et al. 2006 - https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Bounded Version of the Nash-Sutcliffe Efficiency
def nse_c2m(simulation_s, evaluation):
    nse_ = nse(simulation_s, evaluation)
    nse_c2m_ = nse_ / (2 - nse_)

    return nse_c2m_


# Bounded Version of the Original Kling-Gupta Efficiency
def kge_c2m(simulation_s, evaluation):
    kge_ = kge(simulation_s, evaluation)[0, :]
    kge_c2m_ = kge_ / (2 - kge_)

    return kge_c2m_


# Bounded Version of the Modified Kling-Gupta Efficiency
def kgeprime_c2m(simulation_s, evaluation):
    kgeprime_ = kgeprime(simulation_s, evaluation)[0, :]
    kgeprime_c2m_ = kgeprime_ / (2 - kgeprime_)

    return kgeprime_c2m_


# Bounded Version of the Modified Kling-Gupta Efficiency
def kgenp_c2m(simulation_s, evaluation):
    kgenp_ = kgenp(simulation_s, evaluation)[0, :]
    kgenp_c2m_ = kgenp_ / (2 - kgenp_)

    return kgenp_c2m_
