# Copyright (C) 2020  Thibault Hallouin
from setuptools import setup


with open("README.rst", "r") as fd:
    long_desc = fd.read()

with open('hydroeval/version.py') as fv:
    exec(fv.read())

setup(
    name='hydroeval',

    version=__version__,

    description='HydroEval: An Efficient Evaluator for Streamflow Time Series In Python',
    long_description=long_desc,
    long_description_content_type="text/x-rst",

    url='https://thibhlln.github.io/hydroeval',
    project_urls={
        "Documentation": "https://thibhlln.github.io/hydroeval",
        "Source": "https://github.com/thibhlln/hydroeval",
        "Tracker": "https://github.com/thibhlln/hydroeval/issues",
    },

    author='Thibault Hallouin',
    author_email='thibault.hallouin@ucdconnect.ie',

    license='GPLv3',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Natural Language :: English',

        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Hydrology',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',


        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
    ],

    packages=['hydroeval'],

    install_requires=[
        'numpy'
    ],
)
