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

from .resource import Resource


class VirtualNetwork(Resource):
    """Virtual Network resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: Resource ID.
    :type id: str
    :ivar name: Resource name.
    :vartype name: str
    :ivar type: Resource type.
    :vartype type: str
    :param location: Resource location.
    :type location: str
    :param tags: Resource tags.
    :type tags: dict[str, str]
    :param address_space: The AddressSpace that contains an array of IP
     address ranges that can be used by subnets.
    :type address_space: ~azure.mgmt.network.v2017_06_01.models.AddressSpace
    :param dhcp_options: The dhcpOptions that contains an array of DNS servers
     available to VMs deployed in the virtual network.
    :type dhcp_options: ~azure.mgmt.network.v2017_06_01.models.DhcpOptions
    :param subnets: A list of subnets in a Virtual Network.
    :type subnets: list[~azure.mgmt.network.v2017_06_01.models.Subnet]
    :param virtual_network_peerings: A list of peerings in a Virtual Network.
    :type virtual_network_peerings:
     list[~azure.mgmt.network.v2017_06_01.models.VirtualNetworkPeering]
    :param resource_guid: The resourceGuid property of the Virtual Network
     resource.
    :type resource_guid: str
    :param provisioning_state: The provisioning state of the PublicIP
     resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
    :type provisioning_state: str
    :param etag: Gets a unique read-only string that changes whenever the
     resource is updated.
    :type etag: str
    """

    _validation = {
        'name': {'readonly': True},
        'type': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'address_space': {'key': 'properties.addressSpace', 'type': 'AddressSpace'},
        'dhcp_options': {'key': 'properties.dhcpOptions', 'type': 'DhcpOptions'},
        'subnets': {'key': 'properties.subnets', 'type': '[Subnet]'},
        'virtual_network_peerings': {'key': 'properties.virtualNetworkPeerings', 'type': '[VirtualNetworkPeering]'},
        'resource_guid': {'key': 'properties.resourceGuid', 'type': 'str'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(VirtualNetwork, self).__init__(**kwargs)
        self.address_space = kwargs.get('address_space', None)
        self.dhcp_options = kwargs.get('dhcp_options', None)
        self.subnets = kwargs.get('subnets', None)
        self.virtual_network_peerings = kwargs.get('virtual_network_peerings', None)
        self.resource_guid = kwargs.get('resource_guid', None)
        self.provisioning_state = kwargs.get('provisioning_state', None)
        self.etag = kwargs.get('etag', None)
