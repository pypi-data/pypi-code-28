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

try:
    from .application_gateway_sku_py3 import ApplicationGatewaySku
    from .sub_resource_py3 import SubResource
    from .application_gateway_ip_configuration_py3 import ApplicationGatewayIPConfiguration
    from .application_gateway_ssl_certificate_py3 import ApplicationGatewaySslCertificate
    from .application_gateway_frontend_ip_configuration_py3 import ApplicationGatewayFrontendIPConfiguration
    from .application_gateway_frontend_port_py3 import ApplicationGatewayFrontendPort
    from .application_gateway_backend_address_py3 import ApplicationGatewayBackendAddress
    from .backend_address_pool_py3 import BackendAddressPool
    from .inbound_nat_rule_py3 import InboundNatRule
    from .security_rule_py3 import SecurityRule
    from .network_interface_dns_settings_py3 import NetworkInterfaceDnsSettings
    from .network_interface_py3 import NetworkInterface
    from .network_security_group_py3 import NetworkSecurityGroup
    from .route_py3 import Route
    from .route_table_py3 import RouteTable
    from .public_ip_address_dns_settings_py3 import PublicIPAddressDnsSettings
    from .public_ip_address_py3 import PublicIPAddress
    from .ip_configuration_py3 import IPConfiguration
    from .subnet_py3 import Subnet
    from .network_interface_ip_configuration_py3 import NetworkInterfaceIPConfiguration
    from .application_gateway_backend_address_pool_py3 import ApplicationGatewayBackendAddressPool
    from .application_gateway_backend_http_settings_py3 import ApplicationGatewayBackendHttpSettings
    from .application_gateway_http_listener_py3 import ApplicationGatewayHttpListener
    from .application_gateway_path_rule_py3 import ApplicationGatewayPathRule
    from .application_gateway_probe_py3 import ApplicationGatewayProbe
    from .application_gateway_request_routing_rule_py3 import ApplicationGatewayRequestRoutingRule
    from .application_gateway_url_path_map_py3 import ApplicationGatewayUrlPathMap
    from .application_gateway_py3 import ApplicationGateway
    from .resource_py3 import Resource
    from .dns_name_availability_result_py3 import DnsNameAvailabilityResult
    from .express_route_circuit_authorization_py3 import ExpressRouteCircuitAuthorization
    from .express_route_circuit_peering_config_py3 import ExpressRouteCircuitPeeringConfig
    from .express_route_circuit_stats_py3 import ExpressRouteCircuitStats
    from .express_route_circuit_peering_py3 import ExpressRouteCircuitPeering
    from .express_route_circuit_sku_py3 import ExpressRouteCircuitSku
    from .express_route_circuit_service_provider_properties_py3 import ExpressRouteCircuitServiceProviderProperties
    from .express_route_circuit_py3 import ExpressRouteCircuit
    from .express_route_circuit_arp_table_py3 import ExpressRouteCircuitArpTable
    from .express_route_circuit_routes_table_py3 import ExpressRouteCircuitRoutesTable
    from .express_route_service_provider_bandwidths_offered_py3 import ExpressRouteServiceProviderBandwidthsOffered
    from .express_route_service_provider_py3 import ExpressRouteServiceProvider
    from .frontend_ip_configuration_py3 import FrontendIPConfiguration
    from .load_balancing_rule_py3 import LoadBalancingRule
    from .probe_py3 import Probe
    from .inbound_nat_pool_py3 import InboundNatPool
    from .outbound_nat_rule_py3 import OutboundNatRule
    from .load_balancer_py3 import LoadBalancer
    from .error_details_py3 import ErrorDetails
    from .error_py3 import Error
    from .azure_async_operation_result_py3 import AzureAsyncOperationResult
    from .usage_name_py3 import UsageName
    from .usage_py3 import Usage
    from .address_space_py3 import AddressSpace
    from .dhcp_options_py3 import DhcpOptions
    from .virtual_network_py3 import VirtualNetwork
    from .virtual_network_gateway_ip_configuration_py3 import VirtualNetworkGatewayIPConfiguration
    from .virtual_network_gateway_sku_py3 import VirtualNetworkGatewaySku
    from .vpn_client_root_certificate_py3 import VpnClientRootCertificate
    from .vpn_client_revoked_certificate_py3 import VpnClientRevokedCertificate
    from .vpn_client_configuration_py3 import VpnClientConfiguration
    from .bgp_settings_py3 import BgpSettings
    from .virtual_network_gateway_py3 import VirtualNetworkGateway
    from .vpn_client_parameters_py3 import VpnClientParameters
    from .local_network_gateway_py3 import LocalNetworkGateway
    from .virtual_network_gateway_connection_py3 import VirtualNetworkGatewayConnection
    from .connection_shared_key_result_py3 import ConnectionSharedKeyResult
    from .connection_reset_shared_key_py3 import ConnectionResetSharedKey
    from .connection_shared_key_py3 import ConnectionSharedKey
except (SyntaxError, ImportError):
    from .application_gateway_sku import ApplicationGatewaySku
    from .sub_resource import SubResource
    from .application_gateway_ip_configuration import ApplicationGatewayIPConfiguration
    from .application_gateway_ssl_certificate import ApplicationGatewaySslCertificate
    from .application_gateway_frontend_ip_configuration import ApplicationGatewayFrontendIPConfiguration
    from .application_gateway_frontend_port import ApplicationGatewayFrontendPort
    from .application_gateway_backend_address import ApplicationGatewayBackendAddress
    from .backend_address_pool import BackendAddressPool
    from .inbound_nat_rule import InboundNatRule
    from .security_rule import SecurityRule
    from .network_interface_dns_settings import NetworkInterfaceDnsSettings
    from .network_interface import NetworkInterface
    from .network_security_group import NetworkSecurityGroup
    from .route import Route
    from .route_table import RouteTable
    from .public_ip_address_dns_settings import PublicIPAddressDnsSettings
    from .public_ip_address import PublicIPAddress
    from .ip_configuration import IPConfiguration
    from .subnet import Subnet
    from .network_interface_ip_configuration import NetworkInterfaceIPConfiguration
    from .application_gateway_backend_address_pool import ApplicationGatewayBackendAddressPool
    from .application_gateway_backend_http_settings import ApplicationGatewayBackendHttpSettings
    from .application_gateway_http_listener import ApplicationGatewayHttpListener
    from .application_gateway_path_rule import ApplicationGatewayPathRule
    from .application_gateway_probe import ApplicationGatewayProbe
    from .application_gateway_request_routing_rule import ApplicationGatewayRequestRoutingRule
    from .application_gateway_url_path_map import ApplicationGatewayUrlPathMap
    from .application_gateway import ApplicationGateway
    from .resource import Resource
    from .dns_name_availability_result import DnsNameAvailabilityResult
    from .express_route_circuit_authorization import ExpressRouteCircuitAuthorization
    from .express_route_circuit_peering_config import ExpressRouteCircuitPeeringConfig
    from .express_route_circuit_stats import ExpressRouteCircuitStats
    from .express_route_circuit_peering import ExpressRouteCircuitPeering
    from .express_route_circuit_sku import ExpressRouteCircuitSku
    from .express_route_circuit_service_provider_properties import ExpressRouteCircuitServiceProviderProperties
    from .express_route_circuit import ExpressRouteCircuit
    from .express_route_circuit_arp_table import ExpressRouteCircuitArpTable
    from .express_route_circuit_routes_table import ExpressRouteCircuitRoutesTable
    from .express_route_service_provider_bandwidths_offered import ExpressRouteServiceProviderBandwidthsOffered
    from .express_route_service_provider import ExpressRouteServiceProvider
    from .frontend_ip_configuration import FrontendIPConfiguration
    from .load_balancing_rule import LoadBalancingRule
    from .probe import Probe
    from .inbound_nat_pool import InboundNatPool
    from .outbound_nat_rule import OutboundNatRule
    from .load_balancer import LoadBalancer
    from .error_details import ErrorDetails
    from .error import Error
    from .azure_async_operation_result import AzureAsyncOperationResult
    from .usage_name import UsageName
    from .usage import Usage
    from .address_space import AddressSpace
    from .dhcp_options import DhcpOptions
    from .virtual_network import VirtualNetwork
    from .virtual_network_gateway_ip_configuration import VirtualNetworkGatewayIPConfiguration
    from .virtual_network_gateway_sku import VirtualNetworkGatewaySku
    from .vpn_client_root_certificate import VpnClientRootCertificate
    from .vpn_client_revoked_certificate import VpnClientRevokedCertificate
    from .vpn_client_configuration import VpnClientConfiguration
    from .bgp_settings import BgpSettings
    from .virtual_network_gateway import VirtualNetworkGateway
    from .vpn_client_parameters import VpnClientParameters
    from .local_network_gateway import LocalNetworkGateway
    from .virtual_network_gateway_connection import VirtualNetworkGatewayConnection
    from .connection_shared_key_result import ConnectionSharedKeyResult
    from .connection_reset_shared_key import ConnectionResetSharedKey
    from .connection_shared_key import ConnectionSharedKey
from .application_gateway_paged import ApplicationGatewayPaged
from .express_route_circuit_authorization_paged import ExpressRouteCircuitAuthorizationPaged
from .express_route_circuit_peering_paged import ExpressRouteCircuitPeeringPaged
from .express_route_circuit_arp_table_paged import ExpressRouteCircuitArpTablePaged
from .express_route_circuit_routes_table_paged import ExpressRouteCircuitRoutesTablePaged
from .express_route_circuit_stats_paged import ExpressRouteCircuitStatsPaged
from .express_route_circuit_paged import ExpressRouteCircuitPaged
from .express_route_service_provider_paged import ExpressRouteServiceProviderPaged
from .load_balancer_paged import LoadBalancerPaged
from .network_interface_paged import NetworkInterfacePaged
from .network_security_group_paged import NetworkSecurityGroupPaged
from .security_rule_paged import SecurityRulePaged
from .public_ip_address_paged import PublicIPAddressPaged
from .route_table_paged import RouteTablePaged
from .route_paged import RoutePaged
from .usage_paged import UsagePaged
from .virtual_network_paged import VirtualNetworkPaged
from .subnet_paged import SubnetPaged
from .virtual_network_gateway_paged import VirtualNetworkGatewayPaged
from .virtual_network_gateway_connection_paged import VirtualNetworkGatewayConnectionPaged
from .local_network_gateway_paged import LocalNetworkGatewayPaged
from .network_management_client_enums import (
    ApplicationGatewaySkuName,
    ApplicationGatewayTier,
    IPAllocationMethod,
    TransportProtocol,
    SecurityRuleProtocol,
    SecurityRuleAccess,
    SecurityRuleDirection,
    RouteNextHopType,
    ApplicationGatewayProtocol,
    ApplicationGatewayCookieBasedAffinity,
    ApplicationGatewayRequestRoutingRuleType,
    ApplicationGatewayOperationalState,
    AuthorizationUseStatus,
    ExpressRouteCircuitPeeringAdvertisedPublicPrefixState,
    ExpressRouteCircuitPeeringType,
    ExpressRouteCircuitPeeringState,
    ExpressRouteCircuitSkuTier,
    ExpressRouteCircuitSkuFamily,
    ServiceProviderProvisioningState,
    LoadDistribution,
    ProbeProtocol,
    NetworkOperationStatus,
    VirtualNetworkGatewayType,
    VpnType,
    VirtualNetworkGatewaySkuName,
    VirtualNetworkGatewaySkuTier,
    ProcessorArchitecture,
    VirtualNetworkGatewayConnectionType,
    VirtualNetworkGatewayConnectionStatus,
)

__all__ = [
    'ApplicationGatewaySku',
    'SubResource',
    'ApplicationGatewayIPConfiguration',
    'ApplicationGatewaySslCertificate',
    'ApplicationGatewayFrontendIPConfiguration',
    'ApplicationGatewayFrontendPort',
    'ApplicationGatewayBackendAddress',
    'BackendAddressPool',
    'InboundNatRule',
    'SecurityRule',
    'NetworkInterfaceDnsSettings',
    'NetworkInterface',
    'NetworkSecurityGroup',
    'Route',
    'RouteTable',
    'PublicIPAddressDnsSettings',
    'PublicIPAddress',
    'IPConfiguration',
    'Subnet',
    'NetworkInterfaceIPConfiguration',
    'ApplicationGatewayBackendAddressPool',
    'ApplicationGatewayBackendHttpSettings',
    'ApplicationGatewayHttpListener',
    'ApplicationGatewayPathRule',
    'ApplicationGatewayProbe',
    'ApplicationGatewayRequestRoutingRule',
    'ApplicationGatewayUrlPathMap',
    'ApplicationGateway',
    'Resource',
    'DnsNameAvailabilityResult',
    'ExpressRouteCircuitAuthorization',
    'ExpressRouteCircuitPeeringConfig',
    'ExpressRouteCircuitStats',
    'ExpressRouteCircuitPeering',
    'ExpressRouteCircuitSku',
    'ExpressRouteCircuitServiceProviderProperties',
    'ExpressRouteCircuit',
    'ExpressRouteCircuitArpTable',
    'ExpressRouteCircuitRoutesTable',
    'ExpressRouteServiceProviderBandwidthsOffered',
    'ExpressRouteServiceProvider',
    'FrontendIPConfiguration',
    'LoadBalancingRule',
    'Probe',
    'InboundNatPool',
    'OutboundNatRule',
    'LoadBalancer',
    'ErrorDetails',
    'Error',
    'AzureAsyncOperationResult',
    'UsageName',
    'Usage',
    'AddressSpace',
    'DhcpOptions',
    'VirtualNetwork',
    'VirtualNetworkGatewayIPConfiguration',
    'VirtualNetworkGatewaySku',
    'VpnClientRootCertificate',
    'VpnClientRevokedCertificate',
    'VpnClientConfiguration',
    'BgpSettings',
    'VirtualNetworkGateway',
    'VpnClientParameters',
    'LocalNetworkGateway',
    'VirtualNetworkGatewayConnection',
    'ConnectionSharedKeyResult',
    'ConnectionResetSharedKey',
    'ConnectionSharedKey',
    'ApplicationGatewayPaged',
    'ExpressRouteCircuitAuthorizationPaged',
    'ExpressRouteCircuitPeeringPaged',
    'ExpressRouteCircuitArpTablePaged',
    'ExpressRouteCircuitRoutesTablePaged',
    'ExpressRouteCircuitStatsPaged',
    'ExpressRouteCircuitPaged',
    'ExpressRouteServiceProviderPaged',
    'LoadBalancerPaged',
    'NetworkInterfacePaged',
    'NetworkSecurityGroupPaged',
    'SecurityRulePaged',
    'PublicIPAddressPaged',
    'RouteTablePaged',
    'RoutePaged',
    'UsagePaged',
    'VirtualNetworkPaged',
    'SubnetPaged',
    'VirtualNetworkGatewayPaged',
    'VirtualNetworkGatewayConnectionPaged',
    'LocalNetworkGatewayPaged',
    'ApplicationGatewaySkuName',
    'ApplicationGatewayTier',
    'IPAllocationMethod',
    'TransportProtocol',
    'SecurityRuleProtocol',
    'SecurityRuleAccess',
    'SecurityRuleDirection',
    'RouteNextHopType',
    'ApplicationGatewayProtocol',
    'ApplicationGatewayCookieBasedAffinity',
    'ApplicationGatewayRequestRoutingRuleType',
    'ApplicationGatewayOperationalState',
    'AuthorizationUseStatus',
    'ExpressRouteCircuitPeeringAdvertisedPublicPrefixState',
    'ExpressRouteCircuitPeeringType',
    'ExpressRouteCircuitPeeringState',
    'ExpressRouteCircuitSkuTier',
    'ExpressRouteCircuitSkuFamily',
    'ServiceProviderProvisioningState',
    'LoadDistribution',
    'ProbeProtocol',
    'NetworkOperationStatus',
    'VirtualNetworkGatewayType',
    'VpnType',
    'VirtualNetworkGatewaySkuName',
    'VirtualNetworkGatewaySkuTier',
    'ProcessorArchitecture',
    'VirtualNetworkGatewayConnectionType',
    'VirtualNetworkGatewayConnectionStatus',
]
