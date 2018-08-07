# coding: utf-8

"""
    KAMONOHASHI API

    A platform for deep learning  # noqa: E501

    OpenAPI spec version: v1
    Contact: kamonohashi-support@jp.nssol.nssmc.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint

import six


class JobApiModelsEditInputModel(object):
    """NOTE: This class is auto generated by the swagger code generator program.

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
        'memo': 'str'
    }

    attribute_map = {
        'memo': 'memo'
    }

    def __init__(self, memo=None):  # noqa: E501
        """JobApiModelsEditInputModel - a model defined in Swagger"""  # noqa: E501

        self._memo = None
        self.discriminator = None

        if memo is not None:
            self.memo = memo

    @property
    def memo(self):
        """Gets the memo of this JobApiModelsEditInputModel.  # noqa: E501


        :return: The memo of this JobApiModelsEditInputModel.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this JobApiModelsEditInputModel.


        :param memo: The memo of this JobApiModelsEditInputModel.  # noqa: E501
        :type: str
        """

        self._memo = memo

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
        if issubclass(JobApiModelsEditInputModel, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, JobApiModelsEditInputModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
