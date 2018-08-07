# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.5.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class ConfigAuthOutput(object):

    swagger_types = {
        'verify_endpoint': 'str',
        'client_id': 'str',
        'client_secret': 'str',
        'auth_endpoint': 'str',
        'refresh_endpoint': 'str'
    }

    attribute_map = {
        'verify_endpoint': 'verify_endpoint',
        'client_id': 'client_id',
        'client_secret': 'client_secret',
        'auth_endpoint': 'auth_endpoint',
        'refresh_endpoint': 'refresh_endpoint'
    }

    rattribute_map = {
        'verify_endpoint': 'verify_endpoint',
        'client_id': 'client_id',
        'client_secret': 'client_secret',
        'auth_endpoint': 'auth_endpoint',
        'refresh_endpoint': 'refresh_endpoint'
    }

    def __init__(self, verify_endpoint=None, client_id=None, client_secret=None, auth_endpoint=None, refresh_endpoint=None):  # noqa: E501
        """ConfigAuthOutput - a model defined in Swagger"""

        self._verify_endpoint = None
        self._client_id = None
        self._client_secret = None
        self._auth_endpoint = None
        self._refresh_endpoint = None
        self.discriminator = None
        self.alt_discriminator = None

        if verify_endpoint is not None:
            self.verify_endpoint = verify_endpoint
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if auth_endpoint is not None:
            self.auth_endpoint = auth_endpoint
        if refresh_endpoint is not None:
            self.refresh_endpoint = refresh_endpoint

    @property
    def verify_endpoint(self):
        """Gets the verify_endpoint of this ConfigAuthOutput.


        :return: The verify_endpoint of this ConfigAuthOutput.
        :rtype: str
        """
        return self._verify_endpoint

    @verify_endpoint.setter
    def verify_endpoint(self, verify_endpoint):
        """Sets the verify_endpoint of this ConfigAuthOutput.


        :param verify_endpoint: The verify_endpoint of this ConfigAuthOutput.  # noqa: E501
        :type: str
        """

        self._verify_endpoint = verify_endpoint

    @property
    def client_id(self):
        """Gets the client_id of this ConfigAuthOutput.


        :return: The client_id of this ConfigAuthOutput.
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this ConfigAuthOutput.


        :param client_id: The client_id of this ConfigAuthOutput.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def client_secret(self):
        """Gets the client_secret of this ConfigAuthOutput.


        :return: The client_secret of this ConfigAuthOutput.
        :rtype: str
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        """Sets the client_secret of this ConfigAuthOutput.


        :param client_secret: The client_secret of this ConfigAuthOutput.  # noqa: E501
        :type: str
        """

        self._client_secret = client_secret

    @property
    def auth_endpoint(self):
        """Gets the auth_endpoint of this ConfigAuthOutput.


        :return: The auth_endpoint of this ConfigAuthOutput.
        :rtype: str
        """
        return self._auth_endpoint

    @auth_endpoint.setter
    def auth_endpoint(self, auth_endpoint):
        """Sets the auth_endpoint of this ConfigAuthOutput.


        :param auth_endpoint: The auth_endpoint of this ConfigAuthOutput.  # noqa: E501
        :type: str
        """

        self._auth_endpoint = auth_endpoint

    @property
    def refresh_endpoint(self):
        """Gets the refresh_endpoint of this ConfigAuthOutput.


        :return: The refresh_endpoint of this ConfigAuthOutput.
        :rtype: str
        """
        return self._refresh_endpoint

    @refresh_endpoint.setter
    def refresh_endpoint(self, refresh_endpoint):
        """Sets the refresh_endpoint of this ConfigAuthOutput.


        :param refresh_endpoint: The refresh_endpoint of this ConfigAuthOutput.  # noqa: E501
        :type: str
        """

        self._refresh_endpoint = refresh_endpoint


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ConfigAuthOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
