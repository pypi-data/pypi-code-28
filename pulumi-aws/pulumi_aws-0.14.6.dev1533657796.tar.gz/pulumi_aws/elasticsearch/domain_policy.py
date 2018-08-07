# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class DomainPolicy(pulumi.CustomResource):
    """
    Allows setting policy to an ElasticSearch domain while referencing domain attributes (e.g. ARN)
    """
    def __init__(__self__, __name__, __opts__=None, access_policies=None, domain_name=None):
        """Create a DomainPolicy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not access_policies:
            raise TypeError('Missing required property access_policies')
        elif not isinstance(access_policies, basestring):
            raise TypeError('Expected property access_policies to be a basestring')
        __self__.access_policies = access_policies
        """
        IAM policy document specifying the access policies for the domain
        """
        __props__['accessPolicies'] = access_policies

        if not domain_name:
            raise TypeError('Missing required property domain_name')
        elif not isinstance(domain_name, basestring):
            raise TypeError('Expected property domain_name to be a basestring')
        __self__.domain_name = domain_name
        """
        Name of the domain.
        """
        __props__['domainName'] = domain_name

        super(DomainPolicy, __self__).__init__(
            'aws:elasticsearch/domainPolicy:DomainPolicy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'accessPolicies' in outs:
            self.access_policies = outs['accessPolicies']
        if 'domainName' in outs:
            self.domain_name = outs['domainName']
