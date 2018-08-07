# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.5.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from flywheel.api_client import ApiClient
import flywheel.models

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class FilesApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_download_ticket(self, body, **kwargs):  # noqa: E501
        """Create a download ticket

        Use filters in the payload to exclude/include files. To pass a single filter, each of its conditions should be satisfied. If a file pass at least one filter, it is included in the targets. 
        This method makes a synchronous HTTP request by default.

        :param Download body: Download files with tag 'incomplete' OR type 'dicom' (required)
        :param str prefix: A string to customize the name of the download in the format <prefix>_<timestamp>.tar. Defaults to \"scitran\". 
        :param bool async: Perform the request asynchronously
        :return: DownloadTicketWithSummary
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.create_download_ticket_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_download_ticket_with_http_info(body, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def create_download_ticket_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create a download ticket

        Use filters in the payload to exclude/include files. To pass a single filter, each of its conditions should be satisfied. If a file pass at least one filter, it is included in the targets. 
        This method makes a synchronous HTTP request by default.

        :param Download body: Download files with tag 'incomplete' OR type 'dicom' (required)
        :param str prefix: A string to customize the name of the download in the format <prefix>_<timestamp>.tar. Defaults to \"scitran\". 
        :param bool async: Perform the request asynchronously
        :return: DownloadTicketWithSummary
        """

        all_params = ['body', 'prefix']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_download_ticket" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_download_ticket`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'prefix' in params:
            query_params.append(('prefix', params['prefix']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = flywheel.models.Download.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/download', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DownloadTicketWithSummary',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def download_ticket(self, ticket, dest_file, **kwargs):  # noqa: E501
        """Download files listed in the given ticket.

        You can use POST to create a download ticket The files listed in the ticket are put into a tar archive 
        This method makes a synchronous HTTP request by default.

        :param str ticket: ID of the download ticket (required)
        :param str dest_file: Destination file path
        :param bool async: Perform the request asynchronously
        :return: None
        """
        kwargs['_return_http_data_only'] = True
        kwargs['_preload_content'] = False
        # Stream response to file
        with open(dest_file, 'wb') as out_file:
            (resp) = self.download_ticket_with_http_info(ticket, **kwargs)  # noqa: E501
            if resp:
                try:
                    for chunk in resp.iter_content(chunk_size=65536):
                        out_file.write(chunk)
                finally:
                    resp.close()


    def download_ticket_with_http_info(self, ticket, **kwargs):  # noqa: E501
        """Download files listed in the given ticket.

        You can use POST to create a download ticket The files listed in the ticket are put into a tar archive 
        This method makes a synchronous HTTP request by default.

        :param str ticket: ID of the download ticket (required)
        :param bool async: Perform the request asynchronously
        :return: None
        """

        all_params = ['ticket']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method download_ticket" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ticket' is set
        if ('ticket' not in params or
                params['ticket'] is None):
            raise ValueError("Missing the required parameter `ticket` when calling `download_ticket`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ticket' in params:
            query_params.append(('ticket', params['ticket']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/download', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def upload_by_label(self, **kwargs):  # noqa: E501
        """Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior: > For technical reasons, no form field names can be repeated. Instead, use   (file1, file2) and so forth.  > A non-file form field called \"metadata\" is also required, which must be   a string containing JSON.  > See ``api/schemas/input/labelupload.json`` for the format of this metadata.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: object
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.upload_by_label_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.upload_by_label_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def upload_by_label_with_http_info(self, **kwargs):  # noqa: E501
        """Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior: > For technical reasons, no form field names can be repeated. Instead, use   (file1, file2) and so forth.  > A non-file form field called \"metadata\" is also required, which must be   a string containing JSON.  > See ``api/schemas/input/labelupload.json`` for the format of this metadata.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: object
        """

        all_params = ['body', 'form_data', 'ticket']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_by_label" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ticket' in params:
            query_params.append(('ticket', params['ticket']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'body' in params:
            form_params.append(('body', params['body']))  # noqa: E501
        if 'form_data' in params:
            form_params.append(('formData', params['form_data']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/upload/label', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def upload_by_reaper(self, **kwargs):  # noqa: E501
        """Bottom-up UID matching of Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior:  > Upload data, allowing users to move sessions during scans without causing new data to be   created in referenced project/group.  ### Evaluation Order:  * If a matching acquisition UID is found anywhere on the system, the related files will be placed under that acquisition. * **OR** If a matching session UID is found, a new acquistion is created with the specified UID under that Session UID. * **OR** If a matching group ID and project label are found, a new session and acquisition will be created within that project * **OR** If a matching group ID is found, a new project and session and acquisition will be created within that group. * **OR** A new session and acquisition will be created within a special \"Unknown\" group and project, which is only visible to system administrators.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: list[FileEntry]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.upload_by_reaper_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.upload_by_reaper_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def upload_by_reaper_with_http_info(self, **kwargs):  # noqa: E501
        """Bottom-up UID matching of Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior:  > Upload data, allowing users to move sessions during scans without causing new data to be   created in referenced project/group.  ### Evaluation Order:  * If a matching acquisition UID is found anywhere on the system, the related files will be placed under that acquisition. * **OR** If a matching session UID is found, a new acquistion is created with the specified UID under that Session UID. * **OR** If a matching group ID and project label are found, a new session and acquisition will be created within that project * **OR** If a matching group ID is found, a new project and session and acquisition will be created within that group. * **OR** A new session and acquisition will be created within a special \"Unknown\" group and project, which is only visible to system administrators.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: list[FileEntry]
        """

        all_params = ['body', 'form_data', 'ticket']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_by_reaper" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ticket' in params:
            query_params.append(('ticket', params['ticket']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'body' in params:
            form_params.append(('body', params['body']))  # noqa: E501
        if 'form_data' in params:
            form_params.append(('formData', params['form_data']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/upload/reaper', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[FileEntry]',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def upload_by_uid(self, **kwargs):  # noqa: E501
        """Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior: > Same behavior as /api/upload/label,   except the metadata field must be uid format   See ``api/schemas/input/uidupload.json`` for the format of this metadata.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: object
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.upload_by_uid_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.upload_by_uid_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def upload_by_uid_with_http_info(self, **kwargs):  # noqa: E501
        """Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior: > Same behavior as /api/upload/label,   except the metadata field must be uid format   See ``api/schemas/input/uidupload.json`` for the format of this metadata.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: object
        """

        all_params = ['body', 'form_data', 'ticket']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_by_uid" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ticket' in params:
            query_params.append(('ticket', params['ticket']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'body' in params:
            form_params.append(('body', params['body']))  # noqa: E501
        if 'form_data' in params:
            form_params.append(('formData', params['form_data']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/upload/uid', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def upload_match_uid(self, **kwargs):  # noqa: E501
        """Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior: > Accepts uploads to an existing data hierarchy, matched via Session and Acquisition UID   See ``api/schemas/input/uidmatchupload.json`` for the format of this metadata.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: object
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.upload_match_uid_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.upload_match_uid_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def upload_match_uid_with_http_info(self, **kwargs):  # noqa: E501
        """Multipart form upload with N file fields, each with their desired filename.

        ### Default behavior: > Accepts uploads to an existing data hierarchy, matched via Session and Acquisition UID   See ``api/schemas/input/uidmatchupload.json`` for the format of this metadata.  ### Signed URL upload with ``ticket`` > Upload a single file directly to the storage backend. The workflow is the following:    - Send a request with an empty ``?ticket=`` query parameter to get an upload ticket and URL   - Upload the file using a PUT request to the upload URL   - Once done, send a POST request to this endpoint with the upload ticket to finalize the upload.   The file will be placed into the DB via this POST request. 
        This method makes a synchronous HTTP request by default.

        :param str body: Object encoded as a JSON string. It is **required** and used **only** when the ``ticket`` parameter is used. See ``schemas/input/signedurlmetadata.json`` for the format of the json payload. 
        :param str form_data:
        :param str ticket: Use empty value to get a ticket, and provide the ticket id to finalize the upload
        :param bool async: Perform the request asynchronously
        :return: object
        """

        all_params = ['body', 'form_data', 'ticket']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_match_uid" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ticket' in params:
            query_params.append(('ticket', params['ticket']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'body' in params:
            form_params.append(('body', params['body']))  # noqa: E501
        if 'form_data' in params:
            form_params.append(('formData', params['form_data']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/upload/uid-match', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)
