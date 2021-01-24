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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OBJECTIVE FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def nse(simulations, evaluation):
    """Nash-Sutcliffe Efficiency (NSE) as per `Nash and Sutcliffe, 1970
    <https://doi.org/10.1016/0022-1694(70)90255-6>`_.

    :Calculation Details:
        .. math::
           E_{\\text{NSE}} = 1 - \\frac{\\sum_{i=1}^{N}[e_{i}-s_{i}]^2}
           {\\sum_{i=1}^{N}[e_{i}-\\mu(e)]^2}

        where *N* is the length of the *simulations* and *evaluation*
        periods, *e* is the *evaluation* series, *s* is (one of) the
        *simulations* series, and *μ* is the arithmetic mean.

    """
    nse_ = 1 - (
            np.sum((evaluation - simulations) ** 2, axis=0, dtype=np.float64)
            / np.sum((evaluation - np.mean(evaluation)) ** 2, dtype=np.float64)
    )

    return nse_


def kge(simulations, evaluation):
    """Original Kling-Gupta Efficiency (KGE) and its three components
    (r, α, β) as per `Gupta et al., 2009
    <https://doi.org/10.1016/j.jhydrol.2009.08.003>`_.

    Note, all four values KGE, r, α, β are returned, in this order.

    :Calculation Details:
        .. math::
           E_{\\text{KGE}} = 1 - \\sqrt{[r - 1]^2 + [\\alpha - 1]^2
           + [\\beta - 1]^2}
        .. math::
           r = \\frac{\\text{cov}(e, s)}{\\sigma({e}) \\cdot \\sigma(s)}
        .. math::
           \\alpha = \\frac{\\sigma(s)}{\\sigma(e)}
        .. math::
           \\beta = \\frac{\\mu(s)}{\\mu(e)}

        where *e* is the *evaluation* series, *s* is (one of) the
        *simulations* series, *cov* is the covariance, *σ* is the
        standard deviation, and *μ* is the arithmetic mean.

    """
    # calculate error in timing and dynamics r
    # (Pearson's correlation coefficient)
    sim_mean = np.mean(simulations, axis=0, dtype=np.float64)
    obs_mean = np.mean(evaluation, dtype=np.float64)

    r_num = np.sum((simulations - sim_mean) * (evaluation - obs_mean),
                   axis=0, dtype=np.float64)
    r_den = np.sqrt(np.sum((simulations - sim_mean) ** 2,
                           axis=0, dtype=np.float64)
                    * np.sum((evaluation - obs_mean) ** 2,
                             dtype=np.float64))
    r = r_num / r_den
    # calculate error in spread of flow alpha
    alpha = np.std(simulations, axis=0) / np.std(evaluation, dtype=np.float64)
    # calculate error in volume beta (bias of mean discharge)
    beta = (np.sum(simulations, axis=0, dtype=np.float64)
            / np.sum(evaluation, dtype=np.float64))
    # calculate the Kling-Gupta Efficiency KGE
    kge_ = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

    return np.vstack((kge_, r, alpha, beta))


def kgeprime(simulations, evaluation):
    """Modified Kling-Gupta Efficiency (KGE') and its three components
    (r, γ, β) as per `Kling et al., 2012
    <https://doi.org/10.1016/j.jhydrol.2012.01.011>`_.

    Note, all four values KGE', r, γ, β are returned, in this order.

    :Calculation Details:
        .. math::
           E_{\\text{KGE'}} = 1 - \\sqrt{[r - 1]^2 + [\\gamma - 1]^2
           + [\\beta - 1]^2}
        .. math::
           r = \\frac{\\text{cov}(e, s)}{\\sigma({e}) \\cdot \\sigma(s)}
        .. math::
           \\gamma = \\frac{\\sigma(s) / \\mu(s)}{\\sigma(e) / \\mu(e)}
        .. math::
           \\beta = \\frac{\\mu(s)}{\\mu(e)}

        where *e* is the *evaluation* series, *s* is (one of) the
        *simulations* series, *cov* is the covariance, *σ* is the
        standard deviation, and *μ* is the arithmetic mean.

    """
    # calculate error in timing and dynamics r
    # (Pearson's correlation coefficient)
    sim_mean = np.mean(simulations, axis=0, dtype=np.float64)
    obs_mean = np.mean(evaluation, dtype=np.float64)

    r_num = np.sum((simulations - sim_mean) * (evaluation - obs_mean),
                   axis=0, dtype=np.float64)
    r_den = np.sqrt(np.sum((simulations - sim_mean) ** 2,
                           axis=0, dtype=np.float64)
                    * np.sum((evaluation - obs_mean) ** 2,
                             dtype=np.float64))
    r = r_num / r_den

    # calculate error in spread of flow gamma
    # (avoiding cross correlation with bias by dividing by the mean)
    gamma = ((np.std(simulations, axis=0, dtype=np.float64) / sim_mean)
             / (np.std(evaluation, dtype=np.float64) / obs_mean))

    # calculate error in volume beta (bias of mean discharge)
    beta = (np.mean(simulations, axis=0, dtype=np.float64)
            / np.mean(evaluation, axis=0, dtype=np.float64))

    # calculate the modified Kling-Gupta Efficiency KGE'
    kgeprime_ = 1 - np.sqrt((r - 1) ** 2 + (gamma - 1) ** 2 + (beta - 1) ** 2)

    return np.vstack((kgeprime_, r, gamma, beta))


def kgenp(simulations, evaluation):
    """Non-Parametric Kling-Gupta Efficiency (KGE\\ :sub:`NP`\\) and its
    three components (r\\ :sub:`S`\\ , α\\ :sub:`NP`\\, β) as per
    `Pool et al., 2018 <https://doi.org/10.1080/02626667.2018.1552002>`_.

    Note, all four values KGE\\ :sub:`NP`\\, r\\ :sub:`S`\\ , α\\ :sub:`NP`\\,
    β are returned, in this order.

    :Calculation Details:
        .. math::
           E_{\\text{KGE}_\\text{NP}} = 1 - \\sqrt{[r_{\\text{S}} - 1]^2
           + [\\alpha_{\\text{NP}} - 1]^2 + [\\beta - 1]^2}
        .. math::
           r_{\\text{S}} = \\frac{\\sum_{i=1}^{N} [E_i-\\mu(E)] [S_i-\\mu(S)]}
           {\\sqrt{ \\big[ \\sum_{i=1}^{N}[E_i-\\mu(E)]^2 \\big]
           \\big[ \\sum_{i=1}^{N} [S_i-\\mu(S)]^2 \\big]}}
        .. math::
           \\alpha_{\\text{NP}} = 1 - \\frac{1}{2} \\sum_{k=1}^{N}
           \\Bigl| \\frac{s_{I(k)}}{N \\cdot \\mu(s)}
           - \\frac{e_{J(k)}}{N \\cdot \\mu(e)} \\Bigr|
        .. math::
           \\beta = \\frac{\\mu(s)}{\\mu(e)}

        where *N* is the length of the *simulations* and *evaluation*
        periods, *e* is the *evaluation* series, *s* is (one of) the
        *simulations* series, *E* and *S* are the series of ranks for
        the *e* and *s* series of streamflow, respectively, *I* and *J*
        are the functions giving the indices of the *k*\\ :sup:`th` \\
        largest flood in *s* and *e* series, respectively, and *μ* is
        the arithmetic mean.

    """
    # calculate error in timing and dynamics r
    # (Spearman's correlation coefficient)
    sim_rank = np.argsort(np.argsort(simulations, axis=0), axis=0)
    obs_rank = np.argsort(np.argsort(evaluation, axis=0), axis=0)

    r_num = np.sum((obs_rank - np.mean(obs_rank, axis=0, dtype=np.float64))
                   * (sim_rank - np.mean(sim_rank, axis=0, dtype=np.float64)),
                   axis=0)
    r_den = np.sqrt(
        np.sum((obs_rank - np.mean(obs_rank, axis=0, dtype=np.float64)) ** 2,
               axis=0)
        * np.sum((sim_rank - np.mean(sim_rank, axis=0, dtype=np.float64)) ** 2,
                 axis=0)
    )
    r = r_num / r_den

    # calculate error in timing and dynamics alpha (flow duration curve)
    sim_fdc = np.sort(
        simulations / (simulations.shape[0] * np.mean(simulations, axis=0,
                                                      dtype=np.float64)),
        axis=0
    )
    obs_fdc = np.sort(
        evaluation / (evaluation.shape[0] * np.mean(evaluation, axis=0,
                                                    dtype=np.float64)),
        axis=0
    )
    alpha = 1 - 0.5 * np.sum(np.abs(sim_fdc - obs_fdc), axis=0)

    # calculate error in volume beta (bias of mean discharge)
    beta = (np.mean(simulations, axis=0)
            / np.mean(evaluation, axis=0, dtype=np.float64))

    # calculate the non-parametric Kling-Gupta Efficiency KGEnp
    kgenp_ = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

    return np.vstack((kgenp_, r, alpha, beta))


def rmse(simulations, evaluation):
    """Root Mean Square Error (RMSE).

    :Calculation Details:
        .. math::
           E_{\\text{RMSE}} = \\sqrt{\\frac{1}{N}\\sum_{i=1}^{N}[e_i-s_i]^2}

        where *N* is the length of the *simulations* and *evaluation*
        periods, *e* is the *evaluation* series, *s* is (one of) the
        *simulations* series.

    """
    rmse_ = np.sqrt(np.mean((evaluation - simulations) ** 2,
                            axis=0, dtype=np.float64))

    return rmse_


def mare(simulations, evaluation):
    """Mean Absolute Relative Error (MARE).

    :Calculation Details:
        .. math::
           E_{\\text{MARE}} = \\frac{\\sum_{i=1}^{N} \\left| e_i-s_i \\right|}
           {\\sum_{i=1}^{N} e_i}

        where *N* is the length of the *simulations* and *evaluation*
        periods, *e* is the *evaluation* series, *s* is (one of) the
        *simulations* series.

    """
    mare_ = (np.sum(np.abs(evaluation - simulations), axis=0, dtype=np.float64)
             / np.sum(evaluation))

    return mare_


def pbias(simulations, evaluation):
    """Percent Bias (PBias).

    :Calculation Details:
        .. math::
           E_{\\text{PBias}} = 100 × \\frac{\\sum_{i=1}^{N}(e_{i}-s_{i})}{\\sum_{i=1}^{N}e_{i}}

        where *N* is the length of the *simulations* and *evaluation*
        periods, *e* is the *evaluation* series, and *s* is (one of)
        the *simulations* series.

    """
    pbias_ = (100 * np.sum(evaluation - simulations, axis=0, dtype=np.float64)
              / np.sum(evaluation))

    return pbias_

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BOUNDED VERSIONS OF SOME OBJECTIVE FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def nse_c2m(simulations, evaluation):
    """Nash-Sutcliffe Efficiency (NSE) in a bounded version as per
    `Mathevet et al., 2006
    <https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf>`_.

    See `nse` for details on NSE.

    :Calculation Details:
        .. math::
           E_{\\text{NSE,C2M}} = \\frac{E_{\\text{NSE}}}
           {2 - E_{\\text{NSE}}}

    """
    nse_ = nse(simulations, evaluation)
    nse_c2m_ = nse_ / (2 - nse_)

    return nse_c2m_


def kge_c2m(simulations, evaluation):
    """Original Kling-Gupta Efficiency (KGE) in a bounded version as per
    `Mathevet et al., 2006
    <https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf>`_.

    See `kge` for details on KGE.

    Note, only the composite objective function KGE is bounded and
    returned, not its constituents r, α, β.

    :Calculation Details:
        .. math::
           E_{\\text{KGE,C2M}} = \\frac{E_{\\text{KGE}}}
           {2 - E_{\\text{KGE}}}

    """
    kge_ = kge(simulations, evaluation)[0, :]
    kge_c2m_ = kge_ / (2 - kge_)

    return kge_c2m_


def kgeprime_c2m(simulations, evaluation):
    """Modified Kling-Gupta Efficiency (KGE') in a bounded version as
    per `Mathevet et al., 2006
    <https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf>`_.

    See `kgeprime` for details on KGE'.

    Note, only the composite objective function KGE' is bounded and
    returned, not its constituents r, γ, β.

    :Calculation Details:
        .. math::
           E_{\\text{KGE',C2M}} = \\frac{E_{\\text{KGE'}}}
           {2 - E_{\\text{KGE'}}}

    """
    kgeprime_ = kgeprime(simulations, evaluation)[0, :]
    kgeprime_c2m_ = kgeprime_ / (2 - kgeprime_)

    return kgeprime_c2m_


def kgenp_c2m(simulations, evaluation):
    """Non-Parametric Kling-Gupta Efficiency (KGE\\ :sub:`NP`\\) in a bounded
    version as per `Mathevet et al., 2006
    <https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf>`_.

    See `kgenp` for details on KGE\\ :sub:`NP`\\.

    Note, only the composite objective function (KGE\\ :sub:`NP`\\) is bounded
    and returned, not its constituents r\\ :sub:`S`\\ , α\\ :sub:`NP`\\, β.

    :Calculation Details:
        .. math::
           E_{\\text{KGE}_\\text{NP}\\text{,C2M}} = \\frac{E_{\\text{KGE}_\\text{NP}}}
           {2 - E_{\\text{KGE}_\\text{NP}}}

    """
    kgenp_ = kgenp(simulations, evaluation)[0, :]
    kgenp_c2m_ = kgenp_ / (2 - kgenp_)

    return kgenp_c2m_
