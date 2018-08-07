# coding: utf-8

"""
    Connect API

    Mbed Cloud Connect API allows web applications to communicate with devices. You can subscribe to device resources and read/write values to them. Mbed Cloud Connect makes connectivity to devices easy by queuing requests and caching resource values.

    OpenAPI spec version: 2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..api_client import ApiClient


class DeviceRequestsApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_async_request(self, device_id, async_id, body, **kwargs):
        """
        Send an async request to device
        This API provides an interface to asynchronously call methods on a device.  The `async-id` is provided by the client, enabling the client to track the end-to-end flow with an identifier that is relevant to the end application. For example, a web application's session ID along with the device ID and the resource path could be used as the `async-id`. This also avoids any race conditions with [the notification channel](/docs/current/integrate-web-app/event-notification.html). All responses are sent through the currently configured notification channel as an **AsyncIDResponse**.  For `GET` methods, values may be fetched from an internal cache, instead of contacting the device.  See also /v2/endpoints/{device-id}/{resourcePath}.  ``` Example URI: POST /v2/device-requests/015f2fa34d310000000000010030036c?async-id=123e4567-e89b-12d3-a456-426655440000  Example payloads: { \"method\": \"GET\", \"uri\": \"/5/0/1\" } { \"method\": \"PUT\", \"uri\": \"/5/0/1%20?k1=v1&k2=v2%22\", \"accept\": \"text/plain\", \"content-type\": \"text/plain\", \"payload-b64\": \"dmFsdWUxCg==\" }  Immediate response: 202 Accepted  Example AsyncIDResponse, delivered via the notification channel: { \"async-responses\": [ { \"id\": \"123e4567-e89b-12d3-a456-426655440000\", \"status\": 200, \"payload\": \"dmFsdWUxCg==\", \"ct\": \"text/plain\", \"max-age\": 600 } ] } ``` 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.create_async_request(device_id, async_id, body, async=True)
        >>> result = thread.get()

        :param async bool
        :param str device_id: The device ID generated by Mbed Cloud. (required)
        :param str async_id: The client-generated ID for matching the correct response delivered via a notification. (required)
        :param DeviceRequest body: Device request to send. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.create_async_request_with_http_info(device_id, async_id, body, **kwargs)
        else:
            (data) = self.create_async_request_with_http_info(device_id, async_id, body, **kwargs)
            return data

    def create_async_request_with_http_info(self, device_id, async_id, body, **kwargs):
        """
        Send an async request to device
        This API provides an interface to asynchronously call methods on a device.  The `async-id` is provided by the client, enabling the client to track the end-to-end flow with an identifier that is relevant to the end application. For example, a web application's session ID along with the device ID and the resource path could be used as the `async-id`. This also avoids any race conditions with [the notification channel](/docs/current/integrate-web-app/event-notification.html). All responses are sent through the currently configured notification channel as an **AsyncIDResponse**.  For `GET` methods, values may be fetched from an internal cache, instead of contacting the device.  See also /v2/endpoints/{device-id}/{resourcePath}.  ``` Example URI: POST /v2/device-requests/015f2fa34d310000000000010030036c?async-id=123e4567-e89b-12d3-a456-426655440000  Example payloads: { \"method\": \"GET\", \"uri\": \"/5/0/1\" } { \"method\": \"PUT\", \"uri\": \"/5/0/1%20?k1=v1&k2=v2%22\", \"accept\": \"text/plain\", \"content-type\": \"text/plain\", \"payload-b64\": \"dmFsdWUxCg==\" }  Immediate response: 202 Accepted  Example AsyncIDResponse, delivered via the notification channel: { \"async-responses\": [ { \"id\": \"123e4567-e89b-12d3-a456-426655440000\", \"status\": 200, \"payload\": \"dmFsdWUxCg==\", \"ct\": \"text/plain\", \"max-age\": 600 } ] } ``` 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.create_async_request_with_http_info(device_id, async_id, body, async=True)
        >>> result = thread.get()

        :param async bool
        :param str device_id: The device ID generated by Mbed Cloud. (required)
        :param str async_id: The client-generated ID for matching the correct response delivered via a notification. (required)
        :param DeviceRequest body: Device request to send. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['device_id', 'async_id', 'body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_async_request" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'device_id' is set
        if ('device_id' not in params) or (params['device_id'] is None):
            raise ValueError("Missing the required parameter `device_id` when calling `create_async_request`")
        # verify the required parameter 'async_id' is set
        if ('async_id' not in params) or (params['async_id'] is None):
            raise ValueError("Missing the required parameter `async_id` when calling `create_async_request`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_async_request`")

        if 'async_id' in params and not re.search('^[\\w\\-]{1,40}$', params['async_id']):
            raise ValueError("Invalid value for parameter `async_id` when calling `create_async_request`, must conform to the pattern `/^[\\w\\-]{1,40}$/`")

        collection_formats = {}

        path_params = {}
        if 'device_id' in params:
            path_params['device-id'] = params['device_id']

        query_params = []
        if 'async_id' in params:
            query_params.append(('async-id', params['async_id']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['Bearer']

        return self.api_client.call_api('/v2/device-requests/{device-id}', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
