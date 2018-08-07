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

from kamonohashi.models.components_container_image_output_model import \
    ComponentsContainerImageOutputModel  # noqa: F401,E501
from kamonohashi.models.components_git_commit_output_model import ComponentsGitCommitOutputModel  # noqa: F401,E501


class PreprocessingApiModelsDetailsOutputModel(object):
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
        'container_image': 'ComponentsContainerImageOutputModel',
        'created_at': 'str',
        'created_by': 'str',
        'entry_point': 'str',
        'git_model': 'ComponentsGitCommitOutputModel',
        'id': 'int',
        'is_executed': 'bool',
        'memo': 'str',
        'modified_at': 'str',
        'modified_by': 'str',
        'name': 'str'
    }

    attribute_map = {
        'container_image': 'containerImage',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'entry_point': 'entryPoint',
        'git_model': 'gitModel',
        'id': 'id',
        'is_executed': 'isExecuted',
        'memo': 'memo',
        'modified_at': 'modifiedAt',
        'modified_by': 'modifiedBy',
        'name': 'name'
    }

    def __init__(self, container_image=None, created_at=None, created_by=None, entry_point=None, git_model=None, id=None, is_executed=None, memo=None, modified_at=None, modified_by=None, name=None):  # noqa: E501
        """PreprocessingApiModelsDetailsOutputModel - a model defined in Swagger"""  # noqa: E501

        self._container_image = None
        self._created_at = None
        self._created_by = None
        self._entry_point = None
        self._git_model = None
        self._id = None
        self._is_executed = None
        self._memo = None
        self._modified_at = None
        self._modified_by = None
        self._name = None
        self.discriminator = None

        if container_image is not None:
            self.container_image = container_image
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if entry_point is not None:
            self.entry_point = entry_point
        if git_model is not None:
            self.git_model = git_model
        if id is not None:
            self.id = id
        if is_executed is not None:
            self.is_executed = is_executed
        if memo is not None:
            self.memo = memo
        if modified_at is not None:
            self.modified_at = modified_at
        if modified_by is not None:
            self.modified_by = modified_by
        if name is not None:
            self.name = name

    @property
    def container_image(self):
        """Gets the container_image of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The container_image of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: ComponentsContainerImageOutputModel
        """
        return self._container_image

    @container_image.setter
    def container_image(self, container_image):
        """Sets the container_image of this PreprocessingApiModelsDetailsOutputModel.


        :param container_image: The container_image of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: ComponentsContainerImageOutputModel
        """

        self._container_image = container_image

    @property
    def created_at(self):
        """Gets the created_at of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The created_at of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PreprocessingApiModelsDetailsOutputModel.


        :param created_at: The created_at of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The created_by of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this PreprocessingApiModelsDetailsOutputModel.


        :param created_by: The created_by of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def entry_point(self):
        """Gets the entry_point of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The entry_point of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._entry_point

    @entry_point.setter
    def entry_point(self, entry_point):
        """Sets the entry_point of this PreprocessingApiModelsDetailsOutputModel.


        :param entry_point: The entry_point of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._entry_point = entry_point

    @property
    def git_model(self):
        """Gets the git_model of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The git_model of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: ComponentsGitCommitOutputModel
        """
        return self._git_model

    @git_model.setter
    def git_model(self, git_model):
        """Sets the git_model of this PreprocessingApiModelsDetailsOutputModel.


        :param git_model: The git_model of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: ComponentsGitCommitOutputModel
        """

        self._git_model = git_model

    @property
    def id(self):
        """Gets the id of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The id of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PreprocessingApiModelsDetailsOutputModel.


        :param id: The id of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def is_executed(self):
        """Gets the is_executed of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The is_executed of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: bool
        """
        return self._is_executed

    @is_executed.setter
    def is_executed(self, is_executed):
        """Sets the is_executed of this PreprocessingApiModelsDetailsOutputModel.


        :param is_executed: The is_executed of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: bool
        """

        self._is_executed = is_executed

    @property
    def memo(self):
        """Gets the memo of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The memo of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this PreprocessingApiModelsDetailsOutputModel.


        :param memo: The memo of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._memo = memo

    @property
    def modified_at(self):
        """Gets the modified_at of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The modified_at of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this PreprocessingApiModelsDetailsOutputModel.


        :param modified_at: The modified_at of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def modified_by(self):
        """Gets the modified_by of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The modified_by of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """Sets the modified_by of this PreprocessingApiModelsDetailsOutputModel.


        :param modified_by: The modified_by of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._modified_by = modified_by

    @property
    def name(self):
        """Gets the name of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501


        :return: The name of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PreprocessingApiModelsDetailsOutputModel.


        :param name: The name of this PreprocessingApiModelsDetailsOutputModel.  # noqa: E501
        :type: str
        """

        self._name = name

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
        if issubclass(PreprocessingApiModelsDetailsOutputModel, dict):
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
        if not isinstance(other, PreprocessingApiModelsDetailsOutputModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
