# coding: utf-8

"""
    Update Service API

    This is the API documentation for the Mbed deployment service, which is part of the update service.

    OpenAPI spec version: 3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class FirmwareImage(object):
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
        'created_at': 'datetime',
        'datafile': 'str',
        'datafile_checksum': 'str',
        'datafile_size': 'int',
        'description': 'str',
        'etag': 'datetime',
        'id': 'str',
        'name': 'str',
        'object': 'str',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'created_at': 'created_at',
        'datafile': 'datafile',
        'datafile_checksum': 'datafile_checksum',
        'datafile_size': 'datafile_size',
        'description': 'description',
        'etag': 'etag',
        'id': 'id',
        'name': 'name',
        'object': 'object',
        'updated_at': 'updated_at'
    }

    def __init__(self, created_at=None, datafile=None, datafile_checksum=None, datafile_size=None, description=None, etag=None, id=None, name=None, object=None, updated_at=None):
        """
        FirmwareImage - a model defined in Swagger
        """

        self._created_at = created_at
        self._datafile = datafile
        self._datafile_checksum = datafile_checksum
        self._datafile_size = datafile_size
        self._description = description
        self._etag = etag
        self._id = id
        self._name = name
        self._object = object
        self._updated_at = updated_at
        self.discriminator = None

    @property
    def created_at(self):
        """
        Gets the created_at of this FirmwareImage.
        The time the object was created

        :return: The created_at of this FirmwareImage.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this FirmwareImage.
        The time the object was created

        :param created_at: The created_at of this FirmwareImage.
        :type: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")

        self._created_at = created_at

    @property
    def datafile(self):
        """
        Gets the datafile of this FirmwareImage.
        The firmware image file URL

        :return: The datafile of this FirmwareImage.
        :rtype: str
        """
        return self._datafile

    @datafile.setter
    def datafile(self, datafile):
        """
        Sets the datafile of this FirmwareImage.
        The firmware image file URL

        :param datafile: The datafile of this FirmwareImage.
        :type: str
        """
        if datafile is None:
            raise ValueError("Invalid value for `datafile`, must not be `None`")

        self._datafile = datafile

    @property
    def datafile_checksum(self):
        """
        Gets the datafile_checksum of this FirmwareImage.
        Checksum (sha256) generated for the datafile

        :return: The datafile_checksum of this FirmwareImage.
        :rtype: str
        """
        return self._datafile_checksum

    @datafile_checksum.setter
    def datafile_checksum(self, datafile_checksum):
        """
        Sets the datafile_checksum of this FirmwareImage.
        Checksum (sha256) generated for the datafile

        :param datafile_checksum: The datafile_checksum of this FirmwareImage.
        :type: str
        """
        if datafile_checksum is None:
            raise ValueError("Invalid value for `datafile_checksum`, must not be `None`")

        self._datafile_checksum = datafile_checksum

    @property
    def datafile_size(self):
        """
        Gets the datafile_size of this FirmwareImage.
        Size of the datafile in bytes

        :return: The datafile_size of this FirmwareImage.
        :rtype: int
        """
        return self._datafile_size

    @datafile_size.setter
    def datafile_size(self, datafile_size):
        """
        Sets the datafile_size of this FirmwareImage.
        Size of the datafile in bytes

        :param datafile_size: The datafile_size of this FirmwareImage.
        :type: int
        """

        self._datafile_size = datafile_size

    @property
    def description(self):
        """
        Gets the description of this FirmwareImage.
        The description of the object

        :return: The description of this FirmwareImage.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FirmwareImage.
        The description of the object

        :param description: The description of this FirmwareImage.
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")
        if description is not None and len(description) > 2000:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `2000`")

        self._description = description

    @property
    def etag(self):
        """
        Gets the etag of this FirmwareImage.
        The entity instance signature

        :return: The etag of this FirmwareImage.
        :rtype: datetime
        """
        return self._etag

    @etag.setter
    def etag(self, etag):
        """
        Sets the etag of this FirmwareImage.
        The entity instance signature

        :param etag: The etag of this FirmwareImage.
        :type: datetime
        """
        if etag is None:
            raise ValueError("Invalid value for `etag`, must not be `None`")

        self._etag = etag

    @property
    def id(self):
        """
        Gets the id of this FirmwareImage.
        The firmware image ID

        :return: The id of this FirmwareImage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FirmwareImage.
        The firmware image ID

        :param id: The id of this FirmwareImage.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this FirmwareImage.
        The firmware image name

        :return: The name of this FirmwareImage.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FirmwareImage.
        The firmware image name

        :param name: The name of this FirmwareImage.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        if name is not None and len(name) > 128:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `128`")

        self._name = name

    @property
    def object(self):
        """
        Gets the object of this FirmwareImage.
        The API resource entity

        :return: The object of this FirmwareImage.
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this FirmwareImage.
        The API resource entity

        :param object: The object of this FirmwareImage.
        :type: str
        """
        if object is None:
            raise ValueError("Invalid value for `object`, must not be `None`")

        self._object = object

    @property
    def updated_at(self):
        """
        Gets the updated_at of this FirmwareImage.
        The time the object was updated

        :return: The updated_at of this FirmwareImage.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this FirmwareImage.
        The time the object was updated

        :param updated_at: The updated_at of this FirmwareImage.
        :type: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")

        self._updated_at = updated_at

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
        if not isinstance(other, FirmwareImage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
