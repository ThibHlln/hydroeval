.. default-role:: obj

latest
------

Yet to be versioned and released. Only available from *dev* branch until then.

.. rubric:: Tests

* add explicit failing exit code to test suite to let GitHub Actions workflow
  know not all tests succeeded

v0.1.0
------

Released on 2021-04-22.

.. rubric:: General

* drop support for Python 2.7.x

.. rubric:: API changes

* `evaluator` now supports any array-like object, e.g. `numpy.array`, `list`
* rename `evaluator`'s parameter from *simulation_s* to *simulations*
  **[break backwards compatibility]**

.. rubric:: Tests

* add `unittest` test suite to check that new commits do not change results
* add `doctest` tests to check that the API as presented in the docs is working
* add GitHub workflow to run tests

.. rubric:: Documentation

* add a documentation website generated with `sphinx`

v0.0.3
------

Released on 2019-09-08.

.. rubric:: Bug fixes

* add relative imports for non-parametric KGE

.. rubric:: Documentation

* update the tutorial notebook to correct typos

v0.0.2
------

Released on 2018-11-29.

* redefine *axis=0* as default array orientation
* add non-parametric version of KGE
* correct mistake in bounded original and modified KGE

v0.0.1
------

Released on 2018-10-26.

* first release