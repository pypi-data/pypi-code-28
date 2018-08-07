# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class IdentityProvider(pulumi.CustomResource):
    """
    Provides a Cognito User Identity Provider resource.
    """
    def __init__(__self__, __name__, __opts__=None, attribute_mapping=None, idp_identifiers=None, provider_details=None, provider_name=None, provider_type=None, user_pool_id=None):
        """Create a IdentityProvider resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if attribute_mapping and not isinstance(attribute_mapping, dict):
            raise TypeError('Expected property attribute_mapping to be a dict')
        __self__.attribute_mapping = attribute_mapping
        """
        The map of attribute mapping of user pool attributes. [AttributeMapping in AWS API documentation](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-AttributeMapping)
        """
        __props__['attributeMapping'] = attribute_mapping

        if idp_identifiers and not isinstance(idp_identifiers, list):
            raise TypeError('Expected property idp_identifiers to be a list')
        __self__.idp_identifiers = idp_identifiers
        """
        The list of identity providers.
        """
        __props__['idpIdentifiers'] = idp_identifiers

        if not provider_details:
            raise TypeError('Missing required property provider_details')
        elif not isinstance(provider_details, dict):
            raise TypeError('Expected property provider_details to be a dict')
        __self__.provider_details = provider_details
        """
        The map of identity details, such as access token
        """
        __props__['providerDetails'] = provider_details

        if not provider_name:
            raise TypeError('Missing required property provider_name')
        elif not isinstance(provider_name, basestring):
            raise TypeError('Expected property provider_name to be a basestring')
        __self__.provider_name = provider_name
        """
        The provider name
        """
        __props__['providerName'] = provider_name

        if not provider_type:
            raise TypeError('Missing required property provider_type')
        elif not isinstance(provider_type, basestring):
            raise TypeError('Expected property provider_type to be a basestring')
        __self__.provider_type = provider_type
        """
        The provider type.  [See AWS API for valid values](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-ProviderType)
        """
        __props__['providerType'] = provider_type

        if not user_pool_id:
            raise TypeError('Missing required property user_pool_id')
        elif not isinstance(user_pool_id, basestring):
            raise TypeError('Expected property user_pool_id to be a basestring')
        __self__.user_pool_id = user_pool_id
        """
        The user pool id
        """
        __props__['userPoolId'] = user_pool_id

        super(IdentityProvider, __self__).__init__(
            'aws:cognito/identityProvider:IdentityProvider',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'attributeMapping' in outs:
            self.attribute_mapping = outs['attributeMapping']
        if 'idpIdentifiers' in outs:
            self.idp_identifiers = outs['idpIdentifiers']
        if 'providerDetails' in outs:
            self.provider_details = outs['providerDetails']
        if 'providerName' in outs:
            self.provider_name = outs['providerName']
        if 'providerType' in outs:
            self.provider_type = outs['providerType']
        if 'userPoolId' in outs:
            self.user_pool_id = outs['userPoolId']
