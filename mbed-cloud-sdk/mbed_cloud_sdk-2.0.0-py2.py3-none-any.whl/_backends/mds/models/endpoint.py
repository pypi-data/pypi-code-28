# coding: utf-8

"""
    Connect API

    Mbed Cloud Connect API allows web applications to communicate with devices. You can subscribe to device resources and read/write values to them. Mbed Cloud Connect makes connectivity to devices easy by queuing requests and caching resource values.

    OpenAPI spec version: 2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class Endpoint(object):
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
        'name': 'str',
        'q': 'bool',
        'status': 'str',
        'type': 'str'
    }

    attribute_map = {
        'name': 'name',
        'q': 'q',
        'status': 'status',
        'type': 'type'
    }

    def __init__(self, name=None, q=None, status=None, type=None):
        """
        Endpoint - a model defined in Swagger
        """

        self._name = name
        self._q = q
        self._status = status
        self._type = type
        self.discriminator = None

    @property
    def name(self):
        """
        Gets the name of this Endpoint.
        Unique Mbed Cloud Device ID representing the endpoint.

        :return: The name of this Endpoint.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Endpoint.
        Unique Mbed Cloud Device ID representing the endpoint.

        :param name: The name of this Endpoint.
        :type: str
        """

        self._name = name

    @property
    def q(self):
        """
        Gets the q of this Endpoint.
        Determines whether the device is in queue mode. <br/><br/><b>Queue mode</b><br/> When an endpoint is in queue mode, messages sent to the endpoint do not wake up the physical device. The messages are queued and delivered when the device wakes up and connects to Mbed Cloud Connect itself. You can also use the queue mode when the device is behind a NAT and cannot be reached directly by Mbed Cloud Connect. 

        :return: The q of this Endpoint.
        :rtype: bool
        """
        return self._q

    @q.setter
    def q(self, q):
        """
        Sets the q of this Endpoint.
        Determines whether the device is in queue mode. <br/><br/><b>Queue mode</b><br/> When an endpoint is in queue mode, messages sent to the endpoint do not wake up the physical device. The messages are queued and delivered when the device wakes up and connects to Mbed Cloud Connect itself. You can also use the queue mode when the device is behind a NAT and cannot be reached directly by Mbed Cloud Connect. 

        :param q: The q of this Endpoint.
        :type: bool
        """

        self._q = q

    @property
    def status(self):
        """
        Gets the status of this Endpoint.
        Deprecated and the value is always ACTIVE. Only used for API backwards compatibility reasons.

        :return: The status of this Endpoint.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this Endpoint.
        Deprecated and the value is always ACTIVE. Only used for API backwards compatibility reasons.

        :param status: The status of this Endpoint.
        :type: str
        """

        self._status = status

    @property
    def type(self):
        """
        Gets the type of this Endpoint.
        Type of endpoint. (Free text)

        :return: The type of this Endpoint.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Endpoint.
        Type of endpoint. (Free text)

        :param type: The type of this Endpoint.
        :type: str
        """

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
        if not isinstance(other, Endpoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
