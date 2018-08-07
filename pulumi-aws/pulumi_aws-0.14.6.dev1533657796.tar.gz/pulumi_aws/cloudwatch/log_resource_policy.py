# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class LogResourcePolicy(pulumi.CustomResource):
    """
    Provides a resource to manage a CloudWatch log resource policy.
    """
    def __init__(__self__, __name__, __opts__=None, policy_document=None, policy_name=None):
        """Create a LogResourcePolicy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not policy_document:
            raise TypeError('Missing required property policy_document')
        elif not isinstance(policy_document, basestring):
            raise TypeError('Expected property policy_document to be a basestring')
        __self__.policy_document = policy_document
        """
        Details of the resource policy, including the identity of the principal that is enabled to put logs to this account. This is formatted as a JSON string. Maximum length of 5120 characters.
        """
        __props__['policyDocument'] = policy_document

        if not policy_name:
            raise TypeError('Missing required property policy_name')
        elif not isinstance(policy_name, basestring):
            raise TypeError('Expected property policy_name to be a basestring')
        __self__.policy_name = policy_name
        """
        Name of the resource policy.
        """
        __props__['policyName'] = policy_name

        super(LogResourcePolicy, __self__).__init__(
            'aws:cloudwatch/logResourcePolicy:LogResourcePolicy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'policyDocument' in outs:
            self.policy_document = outs['policyDocument']
        if 'policyName' in outs:
            self.policy_name = outs['policyName']
