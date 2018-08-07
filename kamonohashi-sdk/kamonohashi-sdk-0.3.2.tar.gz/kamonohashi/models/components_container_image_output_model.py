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


class ComponentsContainerImageOutputModel(object):
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
        'image': 'str',
        'registry_id': 'int',
        'registry_name': 'str',
        'tag': 'str',
        'url': 'str'
    }

    attribute_map = {
        'image': 'image',
        'registry_id': 'registryId',
        'registry_name': 'registryName',
        'tag': 'tag',
        'url': 'url'
    }

    def __init__(self, image=None, registry_id=None, registry_name=None, tag=None, url=None):  # noqa: E501
        """ComponentsContainerImageOutputModel - a model defined in Swagger"""  # noqa: E501

        self._image = None
        self._registry_id = None
        self._registry_name = None
        self._tag = None
        self._url = None
        self.discriminator = None

        self.image = image
        if registry_id is not None:
            self.registry_id = registry_id
        if registry_name is not None:
            self.registry_name = registry_name
        self.tag = tag
        if url is not None:
            self.url = url

    @property
    def image(self):
        """Gets the image of this ComponentsContainerImageOutputModel.  # noqa: E501


        :return: The image of this ComponentsContainerImageOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this ComponentsContainerImageOutputModel.


        :param image: The image of this ComponentsContainerImageOutputModel.  # noqa: E501
        :type: str
        """
        if image is None:
            raise ValueError("Invalid value for `image`, must not be `None`")  # noqa: E501

        self._image = image

    @property
    def registry_id(self):
        """Gets the registry_id of this ComponentsContainerImageOutputModel.  # noqa: E501


        :return: The registry_id of this ComponentsContainerImageOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._registry_id

    @registry_id.setter
    def registry_id(self, registry_id):
        """Sets the registry_id of this ComponentsContainerImageOutputModel.


        :param registry_id: The registry_id of this ComponentsContainerImageOutputModel.  # noqa: E501
        :type: int
        """

        self._registry_id = registry_id

    @property
    def registry_name(self):
        """Gets the registry_name of this ComponentsContainerImageOutputModel.  # noqa: E501


        :return: The registry_name of this ComponentsContainerImageOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._registry_name

    @registry_name.setter
    def registry_name(self, registry_name):
        """Sets the registry_name of this ComponentsContainerImageOutputModel.


        :param registry_name: The registry_name of this ComponentsContainerImageOutputModel.  # noqa: E501
        :type: str
        """

        self._registry_name = registry_name

    @property
    def tag(self):
        """Gets the tag of this ComponentsContainerImageOutputModel.  # noqa: E501


        :return: The tag of this ComponentsContainerImageOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this ComponentsContainerImageOutputModel.


        :param tag: The tag of this ComponentsContainerImageOutputModel.  # noqa: E501
        :type: str
        """
        if tag is None:
            raise ValueError("Invalid value for `tag`, must not be `None`")  # noqa: E501

        self._tag = tag

    @property
    def url(self):
        """Gets the url of this ComponentsContainerImageOutputModel.  # noqa: E501


        :return: The url of this ComponentsContainerImageOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ComponentsContainerImageOutputModel.


        :param url: The url of this ComponentsContainerImageOutputModel.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(ComponentsContainerImageOutputModel, dict):
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
        if not isinstance(other, ComponentsContainerImageOutputModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
