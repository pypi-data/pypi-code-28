# coding=utf-8
""""""
from __future__ import absolute_import, division, print_function

from .extension import FileUploadsExtension


def register_plugin(app):
    FileUploadsExtension(app)
