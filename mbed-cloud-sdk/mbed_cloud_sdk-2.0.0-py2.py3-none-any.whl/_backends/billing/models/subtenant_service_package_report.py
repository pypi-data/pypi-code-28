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


class SubtenantServicePackageReport(object):
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
        'quota_usage': 'list[QuotaUsageReport]'
    }

    attribute_map = {
        'quota_usage': 'quota_usage'
    }

    def __init__(self, quota_usage=None):
        """
        SubtenantServicePackageReport - a model defined in Swagger
        """

        self._quota_usage = quota_usage
        self.discriminator = None

    @property
    def quota_usage(self):
        """
        Gets the quota_usage of this SubtenantServicePackageReport.

        :return: The quota_usage of this SubtenantServicePackageReport.
        :rtype: list[QuotaUsageReport]
        """
        return self._quota_usage

    @quota_usage.setter
    def quota_usage(self, quota_usage):
        """
        Sets the quota_usage of this SubtenantServicePackageReport.

        :param quota_usage: The quota_usage of this SubtenantServicePackageReport.
        :type: list[QuotaUsageReport]
        """
        if quota_usage is None:
            raise ValueError("Invalid value for `quota_usage`, must not be `None`")

        self._quota_usage = quota_usage

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
        if not isinstance(other, SubtenantServicePackageReport):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
