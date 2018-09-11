#!/usr/bin/env python
""""
The MIT License (MIT)

Copyright (c) 2016 Mikael Magnusson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import setuptools.command.build_py
import setuptools.command.install_lib
import subprocess

from setuptools import setup
import site


class PreBuilder(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        proc = subprocess.Popen(["make"], shell=True)
        proc.communicate()
        setuptools.command.build_py.build_py.run(self)

datafiles= []
for s in site.getsitepackages():
    datafiles.append((s + "/tiipbusclient/", ['makebuild/COPYING', 'makebuild/redis-server']))

setup(
    name='tiipbusclient',
    version='1.0',
    description='tiip bus messaging system',
    keywords='tiip messaging publish subscribe request reply',
    author='Mikael Magnusson',
    author_email='mikael.m.magnusson@gmail.com',
    license='MIT License',
    url="https://github.com/MickMack1983/multicastclient.git",
    packages=['tiipbusclient'],
    requires=[],
    include_package_data=True,
    data_files=datafiles,
    install_requires=["redis"],
    zip_safe=False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    cmdclass = {'build_py': PreBuilder}
)
