# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class GeoMatchSet(pulumi.CustomResource):
    """
    Provides a WAF Regional Geo Match Set Resource
    """
    def __init__(__self__, __name__, __opts__=None, geo_match_constraints=None, name=None):
        """Create a GeoMatchSet resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if geo_match_constraints and not isinstance(geo_match_constraints, list):
            raise TypeError('Expected property geo_match_constraints to be a list')
        __self__.geo_match_constraints = geo_match_constraints
        """
        The Geo Match Constraint objects which contain the country that you want AWS WAF to search for.
        """
        __props__['geoMatchConstraints'] = geo_match_constraints

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name or description of the Geo Match Set.
        """
        __props__['name'] = name

        super(GeoMatchSet, __self__).__init__(
            'aws:wafregional/geoMatchSet:GeoMatchSet',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'geoMatchConstraints' in outs:
            self.geo_match_constraints = outs['geoMatchConstraints']
        if 'name' in outs:
            self.name = outs['name']
