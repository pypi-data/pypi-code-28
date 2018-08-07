"""
    lml
    ~~~~~~~~~~~~~~~~~~~

    Load me later. A lazy loading plugin management system.

    :copyright: (c) 2017-2018 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import logging
from lml._version import __version__  # flake8: noqa
from lml._version import __author__  # flake8: noqa

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        """
          Null handler for logging
          """

        def emit(self, record):
            pass

    logging.getLogger(__name__).addHandler(NullHandler())
