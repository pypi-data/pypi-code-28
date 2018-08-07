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


class DataApiModelsPreprocessHistoryOutputModel(object):
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
        'id': 'int',
        'input_data_id': 'int',
        'input_data_name': 'str',
        'preprocess_id': 'int',
        'preprocess_name': 'str'
    }

    attribute_map = {
        'id': 'id',
        'input_data_id': 'inputDataId',
        'input_data_name': 'inputDataName',
        'preprocess_id': 'preprocessId',
        'preprocess_name': 'preprocessName'
    }

    def __init__(self, id=None, input_data_id=None, input_data_name=None, preprocess_id=None, preprocess_name=None):  # noqa: E501
        """DataApiModelsPreprocessHistoryOutputModel - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._input_data_id = None
        self._input_data_name = None
        self._preprocess_id = None
        self._preprocess_name = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if input_data_id is not None:
            self.input_data_id = input_data_id
        if input_data_name is not None:
            self.input_data_name = input_data_name
        if preprocess_id is not None:
            self.preprocess_id = preprocess_id
        if preprocess_name is not None:
            self.preprocess_name = preprocess_name

    @property
    def id(self):
        """Gets the id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501


        :return: The id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DataApiModelsPreprocessHistoryOutputModel.


        :param id: The id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def input_data_id(self):
        """Gets the input_data_id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501


        :return: The input_data_id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._input_data_id

    @input_data_id.setter
    def input_data_id(self, input_data_id):
        """Sets the input_data_id of this DataApiModelsPreprocessHistoryOutputModel.


        :param input_data_id: The input_data_id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :type: int
        """

        self._input_data_id = input_data_id

    @property
    def input_data_name(self):
        """Gets the input_data_name of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501


        :return: The input_data_name of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._input_data_name

    @input_data_name.setter
    def input_data_name(self, input_data_name):
        """Sets the input_data_name of this DataApiModelsPreprocessHistoryOutputModel.


        :param input_data_name: The input_data_name of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :type: str
        """

        self._input_data_name = input_data_name

    @property
    def preprocess_id(self):
        """Gets the preprocess_id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501


        :return: The preprocess_id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._preprocess_id

    @preprocess_id.setter
    def preprocess_id(self, preprocess_id):
        """Sets the preprocess_id of this DataApiModelsPreprocessHistoryOutputModel.


        :param preprocess_id: The preprocess_id of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :type: int
        """

        self._preprocess_id = preprocess_id

    @property
    def preprocess_name(self):
        """Gets the preprocess_name of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501


        :return: The preprocess_name of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._preprocess_name

    @preprocess_name.setter
    def preprocess_name(self, preprocess_name):
        """Sets the preprocess_name of this DataApiModelsPreprocessHistoryOutputModel.


        :param preprocess_name: The preprocess_name of this DataApiModelsPreprocessHistoryOutputModel.  # noqa: E501
        :type: str
        """

        self._preprocess_name = preprocess_name

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
        if issubclass(DataApiModelsPreprocessHistoryOutputModel, dict):
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
        if not isinstance(other, DataApiModelsPreprocessHistoryOutputModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
