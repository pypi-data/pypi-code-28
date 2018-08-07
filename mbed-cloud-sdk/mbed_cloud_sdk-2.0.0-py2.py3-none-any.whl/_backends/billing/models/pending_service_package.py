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


class PendingServicePackage(object):
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
        'created': 'datetime',
        'expires': 'datetime',
        'firmware_update_count': 'int',
        'id': 'str',
        'modified': 'datetime',
        'previous_id': 'str',
        'start_time': 'datetime'
    }

    attribute_map = {
        'created': 'created',
        'expires': 'expires',
        'firmware_update_count': 'firmware_update_count',
        'id': 'id',
        'modified': 'modified',
        'previous_id': 'previous_id',
        'start_time': 'start_time'
    }

    def __init__(self, created=None, expires=None, firmware_update_count=None, id=None, modified=None, previous_id=None, start_time=None):
        """
        PendingServicePackage - a model defined in Swagger
        """

        self._created = created
        self._expires = expires
        self._firmware_update_count = firmware_update_count
        self._id = id
        self._modified = modified
        self._previous_id = previous_id
        self._start_time = start_time
        self.discriminator = None

    @property
    def created(self):
        """
        Gets the created of this PendingServicePackage.
        Service package creation time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :return: The created of this PendingServicePackage.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this PendingServicePackage.
        Service package creation time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :param created: The created of this PendingServicePackage.
        :type: datetime
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")

        self._created = created

    @property
    def expires(self):
        """
        Gets the expires of this PendingServicePackage.
        Service package expiration time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :return: The expires of this PendingServicePackage.
        :rtype: datetime
        """
        return self._expires

    @expires.setter
    def expires(self, expires):
        """
        Sets the expires of this PendingServicePackage.
        Service package expiration time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :param expires: The expires of this PendingServicePackage.
        :type: datetime
        """
        if expires is None:
            raise ValueError("Invalid value for `expires`, must not be `None`")

        self._expires = expires

    @property
    def firmware_update_count(self):
        """
        Gets the firmware_update_count of this PendingServicePackage.
        Size of firmware update quota of this service package.

        :return: The firmware_update_count of this PendingServicePackage.
        :rtype: int
        """
        return self._firmware_update_count

    @firmware_update_count.setter
    def firmware_update_count(self, firmware_update_count):
        """
        Sets the firmware_update_count of this PendingServicePackage.
        Size of firmware update quota of this service package.

        :param firmware_update_count: The firmware_update_count of this PendingServicePackage.
        :type: int
        """
        if firmware_update_count is None:
            raise ValueError("Invalid value for `firmware_update_count`, must not be `None`")

        self._firmware_update_count = firmware_update_count

    @property
    def id(self):
        """
        Gets the id of this PendingServicePackage.
        ID of this service package.

        :return: The id of this PendingServicePackage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PendingServicePackage.
        ID of this service package.

        :param id: The id of this PendingServicePackage.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def modified(self):
        """
        Gets the modified of this PendingServicePackage.
        Service package latest modified time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :return: The modified of this PendingServicePackage.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """
        Sets the modified of this PendingServicePackage.
        Service package latest modified time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :param modified: The modified of this PendingServicePackage.
        :type: datetime
        """
        if modified is None:
            raise ValueError("Invalid value for `modified`, must not be `None`")

        self._modified = modified

    @property
    def previous_id(self):
        """
        Gets the previous_id of this PendingServicePackage.
        Previous service package ID.

        :return: The previous_id of this PendingServicePackage.
        :rtype: str
        """
        return self._previous_id

    @previous_id.setter
    def previous_id(self, previous_id):
        """
        Sets the previous_id of this PendingServicePackage.
        Previous service package ID.

        :param previous_id: The previous_id of this PendingServicePackage.
        :type: str
        """
        if previous_id is None:
            raise ValueError("Invalid value for `previous_id`, must not be `None`")

        self._previous_id = previous_id

    @property
    def start_time(self):
        """
        Gets the start_time of this PendingServicePackage.
        Service package start time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :return: The start_time of this PendingServicePackage.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this PendingServicePackage.
        Service package start time in RFC3339 date-time with millisecond accuracy and UTC time zone.

        :param start_time: The start_time of this PendingServicePackage.
        :type: datetime
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")

        self._start_time = start_time

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
        if not isinstance(other, PendingServicePackage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
