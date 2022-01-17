.. currentmodule:: hydroeval
.. default-role:: obj

Tutorial
========

Here is a simple example of the usage of the API of `hydroeval` to
assess the goodness of fit between simulated and observed streamflow
time series.

.. code-block:: python
   :caption: Importing the package and checking its version.

   >>> import hydroeval
   >>> print(hydroeval.__version__)
   0.0.3


Load streamflow time series
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example files are provided in the folder *sample_data/* in order for anyone
to reproduce this tutorial. Because this is a NetCDF file, we are going
to use the Python package `netCDF4` to read the data in, but `hydroeval`
is independent of the file format you are working with because it only
requires `numpy.ndarray` as inputs for streamflow time series.

.. code-block:: python
   :caption: Reading in the streamflow dataset.

   >>> from netCDF4 import Dataset
   >>> from cfunits import Units
   >>> with Dataset('sample_data/catchment.sim.flow.nc', 'r', format='NETCDF4') as f:
   ...     sim_flow = f.variables['flow'][:]  # ensemble of simulated streamflow series
   ...     sim_flow_units = Units(f.variables['flow'].units)
   ...     sim_time = f.variables['time'][:]  # timestamps for simulated period
   ...     sim_time_units = Units(f.variables['time'].units, f.variables['time'].calendar)
   >>> print(sim_flow.shape, sim_time.shape)
   (20, 4383) (4383,)
   >>> with Dataset('sample_data/catchment.obs.flow.nc', 'r', format='NETCDF4') as f:
   ...     obs_flow = f.variables['flow'][:]  # observed streamflow series
   ...     obs_flow_units = Units(f.variables['flow'].units)
   ...     obs_time = f.variables['time'][:]  # timestamps for observed period
   ...     obs_time_units = Units(f.variables['time'].units, f.variables['time'].calendar)
   >>> print(obs_flow.shape, obs_time.shape)
   (4383,) (4383,)

It can be a good idea to check that the simulated and observed datasets
feature the same units. To do so, we are going to use the instantiation
of `cfunits.Units` as done above to compare the units.

.. code-block:: python
   :caption: Checking consistency in units.

   >>> sim_flow_units.equals(obs_flow_units)
   True
   >>> sim_time_units.equals(obs_time_units)
   True

It is also useful to check that the datasets are actually covering the same
period, which can be safely done on the timestamps now we know that the
units are equal.

.. code-block:: python
   :caption: Checking consistency in periods covered.

   >>> import numpy
   >>> numpy.array_equal(sim_time, obs_time)
   True


Calculate any available objective function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that the dataset is loaded in memory, it is time to use `hydroeval`
to compare the simulated and observed hydrograph(s). To do so, import
`hydroeval`, which will give you access to its `evaluator`
Python function as well as all objective functions implemented
in `hydroeval` (as Python functions as well).

By default, `hydroeval` expects the time dimension to be on `axis=0`.
In this example, this is not the case, so we need to specify explicitly
that it is on `axis=1`.

For single-component objective functions such as `nse`, the value returned
is either a scalar if only one simulation time series is evaluated, or
a 1-dimensional `numpy.ndarray` if the several simulation time series are
evaluated.

.. code-block:: python
   :caption: Calculating the Nash-Sutcliffe Efficiency `nse`.

   >>> from hydroeval import evaluator, nse
   >>> my_nse = evaluator(nse, sim_flow, obs_flow, axis=1)
   >>> print(my_nse.shape)
   (20,)
   >>> print(my_nse[0])
   0.34650484836206363

.. note::
   `hydroeval` performs pairwise deletion
   when missing values in the observed streamflow timeseries occur. Missing
   values should be set to `numpy.nan` (Not A Number) in the observed numpy
   array for `hydroeval` to be aware of the positions of the values to
   pairwise delete in both observed and simulated time series.

For multi-component objective functions such as `kge` and its variants,
the orientation of the input array is preserved in the output array
(i.e. the time dimension will be reduced to the number of components
in the objective function).

.. code-block:: python
   :caption: Calculating the Kling-Gupta Efficiency `kge` on inverse-transformed flows.

   >>> from hydroeval import evaluator, kge
   >>> my_kge = evaluator(kge, sim_flow, obs_flow, axis=1, transform='inv')
   >>> print(my_kge.shape)
   (20, 4)
   >>> print(my_kge[0, :])
   [0.72655082 0.84278148 0.95663804 1.21949153]
