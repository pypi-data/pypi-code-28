#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['dask', 
                'distributed', 
                'bottleneck', 
                'netCDF4', 
                'xarray', 
                'cartopy', 
                'esmpy', 
                'pyviz', 
                'hvplot', 
                'geoviews', 
                'xgcm', 
                'xesmf']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Mattia Almansi",
    author_email='mattia.almansi@jhu.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="OceanSpy contains algorithms to facilitate extracting information from ocean model output hosted by SciServer.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='oceanspy',
    name='oceanspy',
    packages=find_packages(include=['oceanspy']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/malmans2/oceanspy',
    version='0.0.6',
    zip_safe=False,
)
