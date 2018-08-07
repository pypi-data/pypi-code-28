"""This file is part of the trivago/rebase library.

# Copyright (c) 2018 trivago N.V.
# License: Apache 2.0
# Source: https://github.com/trivago/rebase
# Version: 1.2.0
# Python Version: 3.6
# Author: Yuv Joodhisty <yuvrajsingh.joodhisty@trivago.com>
"""

from rebase.core import Validator


class StringValidator(Validator):
    def properties(self):
        return {
            **super().properties(),
            'message': lambda: '`{value}` is not a valid string'
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if type(value) is not str:
            self.errors.append(self.message.format(value=value))
            is_valid &= False

        return is_valid
