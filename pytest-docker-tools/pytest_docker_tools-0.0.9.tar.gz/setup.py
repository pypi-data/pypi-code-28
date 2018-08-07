#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pytest_docker_tools',
 'pytest_docker_tools.factories',
 'pytest_docker_tools.wrappers']

package_data = \
{'': ['*'], 'pytest_docker_tools': ['contexts/*', 'contexts/scratch/*']}

install_requires = \
['pytest', 'docker']

entry_points = \
{'pytest11': ['docker_tools = pytest_docker_tools.plugin']}

setup(name='pytest_docker_tools',
      version='0.0.9',
      description='An opionated set of helpers for defining Docker integration test environments with py.test fixtures.',
      author='John Carr',
      author_email='john.carr@unrouted.co.uk',
      url='https://github.com/Jc2k/pytest-docker-tools',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
