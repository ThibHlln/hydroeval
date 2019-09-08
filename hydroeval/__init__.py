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

from .hydroeval import evaluator

from .objective_functions import nse, nse_c2m, kge, kge_c2m, kgeprime, kgeprime_c2m, kgenp, kgenp_c2m, rmse, mare, pbias
from .version import __version__
