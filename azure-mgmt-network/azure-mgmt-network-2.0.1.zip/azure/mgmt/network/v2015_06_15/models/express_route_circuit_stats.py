# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ExpressRouteCircuitStats(Model):
    """Contains stats associated with the peering.

    :param bytes_in: Gets BytesIn of the peering.
    :type bytes_in: int
    :param bytes_out: Gets BytesOut of the peering.
    :type bytes_out: int
    """

    _attribute_map = {
        'bytes_in': {'key': 'bytesIn', 'type': 'int'},
        'bytes_out': {'key': 'bytesOut', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(ExpressRouteCircuitStats, self).__init__(**kwargs)
        self.bytes_in = kwargs.get('bytes_in', None)
        self.bytes_out = kwargs.get('bytes_out', None)
