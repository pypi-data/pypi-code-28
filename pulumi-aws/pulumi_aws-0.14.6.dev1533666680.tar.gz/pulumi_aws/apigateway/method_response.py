# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class MethodResponse(pulumi.CustomResource):
    """
    Provides an HTTP Method Response for an API Gateway Resource.
    """
    def __init__(__self__, __name__, __opts__=None, http_method=None, resource_id=None, response_models=None, response_parameters=None, response_parameters_in_json=None, rest_api=None, status_code=None):
        """Create a MethodResponse resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not http_method:
            raise TypeError('Missing required property http_method')
        elif not isinstance(http_method, basestring):
            raise TypeError('Expected property http_method to be a basestring')
        __self__.http_method = http_method
        """
        The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
        """
        __props__['httpMethod'] = http_method

        if not resource_id:
            raise TypeError('Missing required property resource_id')
        elif not isinstance(resource_id, basestring):
            raise TypeError('Expected property resource_id to be a basestring')
        __self__.resource_id = resource_id
        """
        The API resource ID
        """
        __props__['resourceId'] = resource_id

        if response_models and not isinstance(response_models, dict):
            raise TypeError('Expected property response_models to be a dict')
        __self__.response_models = response_models
        """
        A map of the API models used for the response's content type
        """
        __props__['responseModels'] = response_models

        if response_parameters and not isinstance(response_parameters, dict):
            raise TypeError('Expected property response_parameters to be a dict')
        __self__.response_parameters = response_parameters
        """
        A map of response parameters that can be sent to the caller.
        For example: `response_parameters = { "method.response.header.X-Some-Header" = true }`
        would define that the header `X-Some-Header` can be provided on the response.
        """
        __props__['responseParameters'] = response_parameters

        if response_parameters_in_json and not isinstance(response_parameters_in_json, basestring):
            raise TypeError('Expected property response_parameters_in_json to be a basestring')
        __self__.response_parameters_in_json = response_parameters_in_json
        """
        **Deprecated**, use `response_parameters` instead.
        """
        __props__['responseParametersInJson'] = response_parameters_in_json

        if not rest_api:
            raise TypeError('Missing required property rest_api')
        elif not isinstance(rest_api, basestring):
            raise TypeError('Expected property rest_api to be a basestring')
        __self__.rest_api = rest_api
        """
        The ID of the associated REST API
        """
        __props__['restApi'] = rest_api

        if not status_code:
            raise TypeError('Missing required property status_code')
        elif not isinstance(status_code, basestring):
            raise TypeError('Expected property status_code to be a basestring')
        __self__.status_code = status_code
        """
        The HTTP status code
        """
        __props__['statusCode'] = status_code

        super(MethodResponse, __self__).__init__(
            'aws:apigateway/methodResponse:MethodResponse',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'httpMethod' in outs:
            self.http_method = outs['httpMethod']
        if 'resourceId' in outs:
            self.resource_id = outs['resourceId']
        if 'responseModels' in outs:
            self.response_models = outs['responseModels']
        if 'responseParameters' in outs:
            self.response_parameters = outs['responseParameters']
        if 'responseParametersInJson' in outs:
            self.response_parameters_in_json = outs['responseParametersInJson']
        if 'restApi' in outs:
            self.rest_api = outs['restApi']
        if 'statusCode' in outs:
            self.status_code = outs['statusCode']
