# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class LoadBalancerCookieStickinessPolicy(pulumi.CustomResource):
    """
    Provides a load balancer cookie stickiness policy, which allows an ELB to control the sticky session lifetime of the browser.
    """
    def __init__(__self__, __name__, __opts__=None, cookie_expiration_period=None, lb_port=None, load_balancer=None, name=None):
        """Create a LoadBalancerCookieStickinessPolicy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if cookie_expiration_period and not isinstance(cookie_expiration_period, int):
            raise TypeError('Expected property cookie_expiration_period to be a int')
        __self__.cookie_expiration_period = cookie_expiration_period
        """
        The time period after which
        the session cookie should be considered stale, expressed in seconds.
        """
        __props__['cookieExpirationPeriod'] = cookie_expiration_period

        if not lb_port:
            raise TypeError('Missing required property lb_port')
        elif not isinstance(lb_port, int):
            raise TypeError('Expected property lb_port to be a int')
        __self__.lb_port = lb_port
        """
        The load balancer port to which the policy
        should be applied. This must be an active listener on the load
        balancer.
        """
        __props__['lbPort'] = lb_port

        if not load_balancer:
            raise TypeError('Missing required property load_balancer')
        elif not isinstance(load_balancer, basestring):
            raise TypeError('Expected property load_balancer to be a basestring')
        __self__.load_balancer = load_balancer
        """
        The load balancer to which the policy
        should be attached.
        """
        __props__['loadBalancer'] = load_balancer

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the stickiness policy.
        """
        __props__['name'] = name

        super(LoadBalancerCookieStickinessPolicy, __self__).__init__(
            'aws:elasticloadbalancing/loadBalancerCookieStickinessPolicy:LoadBalancerCookieStickinessPolicy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'cookieExpirationPeriod' in outs:
            self.cookie_expiration_period = outs['cookieExpirationPeriod']
        if 'lbPort' in outs:
            self.lb_port = outs['lbPort']
        if 'loadBalancer' in outs:
            self.load_balancer = outs['loadBalancer']
        if 'name' in outs:
            self.name = outs['name']
