# coding: utf-8

"""
    billing REST API documentation

    This document contains the public REST API definitions of the mbed-billing service.

    OpenAPI spec version: 1.4.4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ReportNotFoundErrorResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'code': 'int',
        'message': 'str',
        'object': 'str',
        'request_id': 'str',
        'type': 'str'
    }

    attribute_map = {
        'code': 'code',
        'message': 'message',
        'object': 'object',
        'request_id': 'request_id',
        'type': 'type'
    }

    def __init__(self, code=None, message=None, object=None, request_id=None, type=None):
        """
        ReportNotFoundErrorResponse - a model defined in Swagger
        """

        self._code = code
        self._message = message
        self._object = object
        self._request_id = request_id
        self._type = type
        self.discriminator = None

    @property
    def code(self):
        """
        Gets the code of this ReportNotFoundErrorResponse.
        Response code. Always set to 404.

        :return: The code of this ReportNotFoundErrorResponse.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this ReportNotFoundErrorResponse.
        Response code. Always set to 404.

        :param code: The code of this ReportNotFoundErrorResponse.
        :type: int
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")

        self._code = code

    @property
    def message(self):
        """
        Gets the message of this ReportNotFoundErrorResponse.
        A human readable message with detailed info.

        :return: The message of this ReportNotFoundErrorResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this ReportNotFoundErrorResponse.
        A human readable message with detailed info.

        :param message: The message of this ReportNotFoundErrorResponse.
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")

        self._message = message

    @property
    def object(self):
        """
        Gets the object of this ReportNotFoundErrorResponse.
        Always set to 'error'.

        :return: The object of this ReportNotFoundErrorResponse.
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this ReportNotFoundErrorResponse.
        Always set to 'error'.

        :param object: The object of this ReportNotFoundErrorResponse.
        :type: str
        """
        if object is None:
            raise ValueError("Invalid value for `object`, must not be `None`")
        allowed_values = ["error"]
        if object not in allowed_values:
            raise ValueError(
                "Invalid value for `object` ({0}), must be one of {1}"
                .format(object, allowed_values)
            )

        self._object = object

    @property
    def request_id(self):
        """
        Gets the request_id of this ReportNotFoundErrorResponse.
        Request ID

        :return: The request_id of this ReportNotFoundErrorResponse.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this ReportNotFoundErrorResponse.
        Request ID

        :param request_id: The request_id of this ReportNotFoundErrorResponse.
        :type: str
        """
        if request_id is None:
            raise ValueError("Invalid value for `request_id`, must not be `None`")

        self._request_id = request_id

    @property
    def type(self):
        """
        Gets the type of this ReportNotFoundErrorResponse.
        Error type. Always set to 'report_not_found'.

        :return: The type of this ReportNotFoundErrorResponse.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ReportNotFoundErrorResponse.
        Error type. Always set to 'report_not_found'.

        :param type: The type of this ReportNotFoundErrorResponse.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")
        allowed_values = ["report_not_found"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

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
        if not isinstance(other, ReportNotFoundErrorResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
