# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class FaxSendRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FaxSendRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'addresses': 'list[str]',
            'document_id': 'str',
            'content_type': 'str',
            'workspace': 'Workspace',
            'cover_sheet': 'CoverSheet',
            'time_zone_offset_minutes': 'int',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'addresses': 'addresses',
            'document_id': 'documentId',
            'content_type': 'contentType',
            'workspace': 'workspace',
            'cover_sheet': 'coverSheet',
            'time_zone_offset_minutes': 'timeZoneOffsetMinutes',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._addresses = None
        self._document_id = None
        self._content_type = None
        self._workspace = None
        self._cover_sheet = None
        self._time_zone_offset_minutes = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this FaxSendRequest.
        The globally unique identifier for the object.

        :return: The id of this FaxSendRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FaxSendRequest.
        The globally unique identifier for the object.

        :param id: The id of this FaxSendRequest.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this FaxSendRequest.


        :return: The name of this FaxSendRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FaxSendRequest.


        :param name: The name of this FaxSendRequest.
        :type: str
        """
        
        self._name = name

    @property
    def addresses(self):
        """
        Gets the addresses of this FaxSendRequest.
        A list of outbound fax dialing addresses. E.g. +13175555555 or 3175555555

        :return: The addresses of this FaxSendRequest.
        :rtype: list[str]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """
        Sets the addresses of this FaxSendRequest.
        A list of outbound fax dialing addresses. E.g. +13175555555 or 3175555555

        :param addresses: The addresses of this FaxSendRequest.
        :type: list[str]
        """
        
        self._addresses = addresses

    @property
    def document_id(self):
        """
        Gets the document_id of this FaxSendRequest.
        DocumentId of Content Management artifact. If Content Management document is not used for faxing, documentId should be null

        :return: The document_id of this FaxSendRequest.
        :rtype: str
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """
        Sets the document_id of this FaxSendRequest.
        DocumentId of Content Management artifact. If Content Management document is not used for faxing, documentId should be null

        :param document_id: The document_id of this FaxSendRequest.
        :type: str
        """
        
        self._document_id = document_id

    @property
    def content_type(self):
        """
        Gets the content_type of this FaxSendRequest.
        The content type that is going to be uploaded. If Content Management document is used for faxing, contentType will be ignored

        :return: The content_type of this FaxSendRequest.
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """
        Sets the content_type of this FaxSendRequest.
        The content type that is going to be uploaded. If Content Management document is used for faxing, contentType will be ignored

        :param content_type: The content_type of this FaxSendRequest.
        :type: str
        """
        allowed_values = ["application/pdf", "image/tiff", "application/msword", "application/vnd.oasis.opendocument.text", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if content_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for content_type -> " + content_type
            self._content_type = "outdated_sdk_version"
        else:
            self._content_type = content_type

    @property
    def workspace(self):
        """
        Gets the workspace of this FaxSendRequest.
        Workspace in which the document should be stored. If Content Management document is used for faxing, workspace will be ignored

        :return: The workspace of this FaxSendRequest.
        :rtype: Workspace
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """
        Sets the workspace of this FaxSendRequest.
        Workspace in which the document should be stored. If Content Management document is used for faxing, workspace will be ignored

        :param workspace: The workspace of this FaxSendRequest.
        :type: Workspace
        """
        
        self._workspace = workspace

    @property
    def cover_sheet(self):
        """
        Gets the cover_sheet of this FaxSendRequest.
        Data for coversheet generation.

        :return: The cover_sheet of this FaxSendRequest.
        :rtype: CoverSheet
        """
        return self._cover_sheet

    @cover_sheet.setter
    def cover_sheet(self, cover_sheet):
        """
        Sets the cover_sheet of this FaxSendRequest.
        Data for coversheet generation.

        :param cover_sheet: The cover_sheet of this FaxSendRequest.
        :type: CoverSheet
        """
        
        self._cover_sheet = cover_sheet

    @property
    def time_zone_offset_minutes(self):
        """
        Gets the time_zone_offset_minutes of this FaxSendRequest.
        Time zone offset minutes from GMT

        :return: The time_zone_offset_minutes of this FaxSendRequest.
        :rtype: int
        """
        return self._time_zone_offset_minutes

    @time_zone_offset_minutes.setter
    def time_zone_offset_minutes(self, time_zone_offset_minutes):
        """
        Sets the time_zone_offset_minutes of this FaxSendRequest.
        Time zone offset minutes from GMT

        :param time_zone_offset_minutes: The time_zone_offset_minutes of this FaxSendRequest.
        :type: int
        """
        
        self._time_zone_offset_minutes = time_zone_offset_minutes

    @property
    def self_uri(self):
        """
        Gets the self_uri of this FaxSendRequest.
        The URI for this object

        :return: The self_uri of this FaxSendRequest.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this FaxSendRequest.
        The URI for this object

        :param self_uri: The self_uri of this FaxSendRequest.
        :type: str
        """
        
        self._self_uri = self_uri

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

