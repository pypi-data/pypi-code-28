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


class PacketCaptureFilter(Model):
    """Filter that is applied to packet capture request. Multiple filters can be
    applied.

    :param protocol: Protocol to be filtered on. Possible values include:
     'TCP', 'UDP', 'Any'. Default value: "Any" .
    :type protocol: str or ~azure.mgmt.network.v2016_09_01.models.PcProtocol
    :param local_ip_address: Local IP Address to be filtered on. Notation:
     "127.0.0.1" for single address entry. "127.0.0.1-127.0.0.255" for range.
     "127.0.0.1;127.0.0.5"? for multiple entries. Multiple ranges not currently
     supported. Mixing ranges with multiple entries not currently supported.
     Default = null.
    :type local_ip_address: str
    :param remote_ip_address: Local IP Address to be filtered on. Notation:
     "127.0.0.1" for single address entry. "127.0.0.1-127.0.0.255" for range.
     "127.0.0.1;127.0.0.5;" for multiple entries. Multiple ranges not currently
     supported. Mixing ranges with multiple entries not currently supported.
     Default = null.
    :type remote_ip_address: str
    :param local_port: Local port to be filtered on. Notation: "80" for single
     port entry."80-85" for range. "80;443;" for multiple entries. Multiple
     ranges not currently supported. Mixing ranges with multiple entries not
     currently supported. Default = null.
    :type local_port: str
    :param remote_port: Remote port to be filtered on. Notation: "80" for
     single port entry."80-85" for range. "80;443;" for multiple entries.
     Multiple ranges not currently supported. Mixing ranges with multiple
     entries not currently supported. Default = null.
    :type remote_port: str
    """

    _attribute_map = {
        'protocol': {'key': 'protocol', 'type': 'str'},
        'local_ip_address': {'key': 'localIPAddress', 'type': 'str'},
        'remote_ip_address': {'key': 'remoteIPAddress', 'type': 'str'},
        'local_port': {'key': 'localPort', 'type': 'str'},
        'remote_port': {'key': 'remotePort', 'type': 'str'},
    }

    def __init__(self, *, protocol="Any", local_ip_address: str=None, remote_ip_address: str=None, local_port: str=None, remote_port: str=None, **kwargs) -> None:
        super(PacketCaptureFilter, self).__init__(**kwargs)
        self.protocol = protocol
        self.local_ip_address = local_ip_address
        self.remote_ip_address = remote_ip_address
        self.local_port = local_port
        self.remote_port = remote_port
