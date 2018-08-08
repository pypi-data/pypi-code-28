#!/usr/bin/env python

"""
Setup file for the Aurora plotting package: TOPAZ
"""
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topaz",
    version="0.0.3",
    author="Adam Batten",
    author_email="adamjbatten@gmail.com",
    description="A plotting package for the Aurora simulations using pynbody",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/abatten/topaz",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
