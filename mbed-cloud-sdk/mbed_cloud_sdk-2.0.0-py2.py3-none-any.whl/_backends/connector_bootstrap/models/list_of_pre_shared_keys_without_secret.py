# coding: utf-8

"""
    Bootstrap API

    Mbed Cloud Bootstrap API allows web applications to control the device bootstrapping process.

    OpenAPI spec version: 2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ListOfPreSharedKeysWithoutSecret(object):
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
        'after': 'str',
        'continuation_marker': 'str',
        'data': 'list[PreSharedKeyWithoutSecret]',
        'has_more': 'bool',
        'limit': 'int',
        'object': 'str',
        'order': 'str'
    }

    attribute_map = {
        'after': 'after',
        'continuation_marker': 'continuation_marker',
        'data': 'data',
        'has_more': 'has_more',
        'limit': 'limit',
        'object': 'object',
        'order': 'order'
    }

    def __init__(self, after=None, continuation_marker=None, data=None, has_more=None, limit=None, object=None, order=None):
        """
        ListOfPreSharedKeysWithoutSecret - a model defined in Swagger
        """

        self._after = after
        self._continuation_marker = continuation_marker
        self._data = data
        self._has_more = has_more
        self._limit = limit
        self._object = object
        self._order = order
        self.discriminator = None

    @property
    def after(self):
        """
        Gets the after of this ListOfPreSharedKeysWithoutSecret.
        An offset token for current page.

        :return: The after of this ListOfPreSharedKeysWithoutSecret.
        :rtype: str
        """
        return self._after

    @after.setter
    def after(self, after):
        """
        Sets the after of this ListOfPreSharedKeysWithoutSecret.
        An offset token for current page.

        :param after: The after of this ListOfPreSharedKeysWithoutSecret.
        :type: str
        """

        self._after = after

    @property
    def continuation_marker(self):
        """
        Gets the continuation_marker of this ListOfPreSharedKeysWithoutSecret.
        An offset token for fetching the next page. Note that exactly the same limit needs to be used on the request for fetching the subsequent pages.

        :return: The continuation_marker of this ListOfPreSharedKeysWithoutSecret.
        :rtype: str
        """
        return self._continuation_marker

    @continuation_marker.setter
    def continuation_marker(self, continuation_marker):
        """
        Sets the continuation_marker of this ListOfPreSharedKeysWithoutSecret.
        An offset token for fetching the next page. Note that exactly the same limit needs to be used on the request for fetching the subsequent pages.

        :param continuation_marker: The continuation_marker of this ListOfPreSharedKeysWithoutSecret.
        :type: str
        """

        self._continuation_marker = continuation_marker

    @property
    def data(self):
        """
        Gets the data of this ListOfPreSharedKeysWithoutSecret.
        Array of the pre-shared key entries. The array is empty if there are no pre-shared keys.

        :return: The data of this ListOfPreSharedKeysWithoutSecret.
        :rtype: list[PreSharedKeyWithoutSecret]
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this ListOfPreSharedKeysWithoutSecret.
        Array of the pre-shared key entries. The array is empty if there are no pre-shared keys.

        :param data: The data of this ListOfPreSharedKeysWithoutSecret.
        :type: list[PreSharedKeyWithoutSecret]
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")

        self._data = data

    @property
    def has_more(self):
        """
        Gets the has_more of this ListOfPreSharedKeysWithoutSecret.
        Are there more results available.

        :return: The has_more of this ListOfPreSharedKeysWithoutSecret.
        :rtype: bool
        """
        return self._has_more

    @has_more.setter
    def has_more(self, has_more):
        """
        Sets the has_more of this ListOfPreSharedKeysWithoutSecret.
        Are there more results available.

        :param has_more: The has_more of this ListOfPreSharedKeysWithoutSecret.
        :type: bool
        """
        if has_more is None:
            raise ValueError("Invalid value for `has_more`, must not be `None`")

        self._has_more = has_more

    @property
    def limit(self):
        """
        Gets the limit of this ListOfPreSharedKeysWithoutSecret.
        The value of limit query parameter from the request, or default if not specified.

        :return: The limit of this ListOfPreSharedKeysWithoutSecret.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """
        Sets the limit of this ListOfPreSharedKeysWithoutSecret.
        The value of limit query parameter from the request, or default if not specified.

        :param limit: The limit of this ListOfPreSharedKeysWithoutSecret.
        :type: int
        """
        if limit is None:
            raise ValueError("Invalid value for `limit`, must not be `None`")

        self._limit = limit

    @property
    def object(self):
        """
        Gets the object of this ListOfPreSharedKeysWithoutSecret.
        The type of this API object is a \"list\".

        :return: The object of this ListOfPreSharedKeysWithoutSecret.
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this ListOfPreSharedKeysWithoutSecret.
        The type of this API object is a \"list\".

        :param object: The object of this ListOfPreSharedKeysWithoutSecret.
        :type: str
        """
        if object is None:
            raise ValueError("Invalid value for `object`, must not be `None`")

        self._object = object

    @property
    def order(self):
        """
        Gets the order of this ListOfPreSharedKeysWithoutSecret.
        The creation time based order of the entries.

        :return: The order of this ListOfPreSharedKeysWithoutSecret.
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """
        Sets the order of this ListOfPreSharedKeysWithoutSecret.
        The creation time based order of the entries.

        :param order: The order of this ListOfPreSharedKeysWithoutSecret.
        :type: str
        """
        if order is None:
            raise ValueError("Invalid value for `order`, must not be `None`")

        self._order = order

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
        if not isinstance(other, ListOfPreSharedKeysWithoutSecret):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
