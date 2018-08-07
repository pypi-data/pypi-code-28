# -*- coding: utf-8 -*-
# Copyright 2018 NS Solutions Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, absolute_import, with_statement

import logging
import logging.handlers
import os
import sys

import click
import pkg_resources
import six

import cli.account
import cli.cluster
import cli.data
import cli.data_set
import cli.job
import cli.preprocessing
import cli.registry
import kamonohashi.rest

name = 'kamonohashi-cli'
version = pkg_resources.get_distribution(name).version
sdk_name = 'kamonohashi-sdk'
sdk_version = pkg_resources.get_distribution(sdk_name).version


def configure_logger():
    """Configure root logger."""
    log_dir_path = os.path.join(os.path.expanduser('~'), '.kqi')
    log_file_path = os.path.join(log_dir_path, 'kqi.log')

    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    encoding = None if six.PY2 else 'utf-8'
    handler = logging.handlers.TimedRotatingFileHandler(log_file_path, when='D', backupCount=10, encoding=encoding)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@click.group(context_settings=dict(help_option_names=['-h', '--help']),
             help='KAMONOHASHI Command Line Interface. version: {version}'.format(version=version))
def kqi():
    pass


kqi.add_command(cli.account.account)
kqi.add_command(cli.cluster.cluster)
kqi.add_command(cli.data_set.data_set, 'dataset')
kqi.add_command(cli.data.data)
kqi.add_command(cli.job.job)
kqi.add_command(cli.registry.registry)
kqi.add_command(cli.preprocessing.preprocessing)


def kqi_main():
    configure_logger()
    try:
        logging.info('%s: %s', name, version)
        logging.info('%s: %s', sdk_name, sdk_version)
        logging.info('sys.platform: %s', sys.platform)
        logging.info('sys.version: %s', sys.version)
        for arg in sys.argv:
            logging.info('sys.argv: %s', arg)
        kqi()
        return 0
    except kamonohashi.rest.ApiException as error:
        if six.PY3 and error.body and isinstance(error.body, bytes):
            error.body = error.body.decode('utf-8')
        print('[ERROR]', error.status, error.reason)
        print(error.body)
        logging.exception(error)
    except Exception as error:
        print('[ERROR]', error)
        logging.exception(error)
    return 1


if __name__ == "__main__":
    # for pydevd & python2 glitch
    kqi(sys.argv[1:])
