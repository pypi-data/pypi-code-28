# coding: utf-8

"""
    Account Management API

    API for managing accounts, users, creating API keys, uploading trusted certificates

    OpenAPI spec version: v3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class GroupCreationInfo(object):
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
        'members': 'SubjectList',
        'name': 'str'
    }

    attribute_map = {
        'members': 'members',
        'name': 'name'
    }

    def __init__(self, members=None, name=None):
        """
        GroupCreationInfo - a model defined in Swagger
        """

        self._members = members
        self._name = name
        self.discriminator = None

    @property
    def members(self):
        """
        Gets the members of this GroupCreationInfo.
        The members of the group as arrays of user and API key UUIDs.

        :return: The members of this GroupCreationInfo.
        :rtype: SubjectList
        """
        return self._members

    @members.setter
    def members(self, members):
        """
        Sets the members of this GroupCreationInfo.
        The members of the group as arrays of user and API key UUIDs.

        :param members: The members of this GroupCreationInfo.
        :type: SubjectList
        """

        self._members = members

    @property
    def name(self):
        """
        Gets the name of this GroupCreationInfo.
        The group name, not longer than 100 characters.

        :return: The name of this GroupCreationInfo.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this GroupCreationInfo.
        The group name, not longer than 100 characters.

        :param name: The name of this GroupCreationInfo.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

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
        if not isinstance(other, GroupCreationInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
