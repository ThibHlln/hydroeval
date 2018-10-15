# -*- coding: utf-8 -*-

# This file is part of HydroEval: An Evaluator for Hydrological Time Series
# Copyright (C) 2018  Thibault Hallouin (1)
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
    nse_ = 1 - (np.sum((evaluation - simulation_s) ** 2, axis=1, dtype=np.float64) /
                np.sum((evaluation - np.mean(evaluation)) ** 2))

    return nse_


# Original Kling-Gupta Efficiency (Gupta et al. 2009 - https://doi.org/10.1016/j.jhydrol.2009.08.003)
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


# Modified kling-Gupta Efficiency (kling et al. 2012 - https://doi.org/10.1016/j.jhydrol.2012.01.011)
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


# Root Mean Square Error
def rmse(simulation_s, evaluation):
    rmse_ = np.sqrt(np.mean((evaluation - simulation_s) ** 2, axis=1, dtype=np.float64))

    return rmse_


# Mean Absolute Relative Error
def mare(simulation_s, evaluation):
    mare_ = np.sum(np.abs(evaluation - simulation_s), axis=1, dtype=np.float64) / np.sum(evaluation)

    return mare_


# Percent Bias
def pbias(simulation_s, evaluation):
    pbias_ = 100 * np.sum(evaluation - simulation_s, axis=1, dtype=np.float64) / np.sum(evaluation)

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
    kge_ = kge(simulation_s, evaluation)[0]
    kge_c2m_ = kge_ / (2 - kge_)

    return kge_c2m_


# Bounded Version of the Modified Kling-Gupta Efficiency
def kgeprime_c2m(simulation_s, evaluation):
    kgeprime_ = kgeprime(simulation_s, evaluation)[0]
    kgeprime_c2m_ = kgeprime_ / (2 - kgeprime_)

    return kgeprime_c2m_
