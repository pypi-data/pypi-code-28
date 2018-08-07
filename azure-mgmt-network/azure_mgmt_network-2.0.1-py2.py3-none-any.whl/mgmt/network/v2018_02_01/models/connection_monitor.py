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


class ConnectionMonitor(Model):
    """Parameters that define the operation to create a connection monitor.

    All required parameters must be populated in order to send to Azure.

    :param location: Connection monitor location.
    :type location: str
    :param tags: Connection monitor tags.
    :type tags: dict[str, str]
    :param source: Required.
    :type source:
     ~azure.mgmt.network.v2018_02_01.models.ConnectionMonitorSource
    :param destination: Required.
    :type destination:
     ~azure.mgmt.network.v2018_02_01.models.ConnectionMonitorDestination
    :param auto_start: Determines if the connection monitor will start
     automatically once created. Default value: True .
    :type auto_start: bool
    :param monitoring_interval_in_seconds: Monitoring interval in seconds.
     Default value: 60 .
    :type monitoring_interval_in_seconds: int
    """

    _validation = {
        'source': {'required': True},
        'destination': {'required': True},
    }

    _attribute_map = {
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'source': {'key': 'properties.source', 'type': 'ConnectionMonitorSource'},
        'destination': {'key': 'properties.destination', 'type': 'ConnectionMonitorDestination'},
        'auto_start': {'key': 'properties.autoStart', 'type': 'bool'},
        'monitoring_interval_in_seconds': {'key': 'properties.monitoringIntervalInSeconds', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(ConnectionMonitor, self).__init__(**kwargs)
        self.location = kwargs.get('location', None)
        self.tags = kwargs.get('tags', None)
        self.source = kwargs.get('source', None)
        self.destination = kwargs.get('destination', None)
        self.auto_start = kwargs.get('auto_start', True)
        self.monitoring_interval_in_seconds = kwargs.get('monitoring_interval_in_seconds', 60)
