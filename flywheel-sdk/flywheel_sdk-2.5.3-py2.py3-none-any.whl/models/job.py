# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.5.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

from flywheel.models.gear_info import GearInfo  # noqa: F401,E501
from flywheel.models.job_config import JobConfig  # noqa: F401,E501
from flywheel.models.job_destination import JobDestination  # noqa: F401,E501
from flywheel.models.job_inputs_object import JobInputsObject  # noqa: F401,E501
from flywheel.models.job_origin import JobOrigin  # noqa: F401,E501
from flywheel.models.job_produced_metadata import JobProducedMetadata  # noqa: F401,E501
from flywheel.models.job_request import JobRequest  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class Job(object):

    swagger_types = {
        'id': 'str',
        'origin': 'JobOrigin',
        'gear_id': 'str',
        'gear_info': 'GearInfo',
        'previous_job_id': 'str',
        'inputs': 'JobInputsObject',
        'destination': 'JobDestination',
        'tags': 'list[str]',
        'state': 'str',
        'attempt': 'int',
        'created': 'datetime',
        'modified': 'datetime',
        'config': 'JobConfig',
        'request': 'JobRequest',
        'saved_files': 'list[str]',
        'produced_metadata': 'JobProducedMetadata'
    }

    attribute_map = {
        'id': 'id',
        'origin': 'origin',
        'gear_id': 'gear_id',
        'gear_info': 'gear_info',
        'previous_job_id': 'previous_job_id',
        'inputs': 'inputs',
        'destination': 'destination',
        'tags': 'tags',
        'state': 'state',
        'attempt': 'attempt',
        'created': 'created',
        'modified': 'modified',
        'config': 'config',
        'request': 'request',
        'saved_files': 'saved_files',
        'produced_metadata': 'produced_metadata'
    }

    rattribute_map = {
        'id': 'id',
        'origin': 'origin',
        'gear_id': 'gear_id',
        'gear_info': 'gear_info',
        'previous_job_id': 'previous_job_id',
        'inputs': 'inputs',
        'destination': 'destination',
        'tags': 'tags',
        'state': 'state',
        'attempt': 'attempt',
        'created': 'created',
        'modified': 'modified',
        'config': 'config',
        'request': 'request',
        'saved_files': 'saved_files',
        'produced_metadata': 'produced_metadata'
    }

    def __init__(self, id=None, origin=None, gear_id=None, gear_info=None, previous_job_id=None, inputs=None, destination=None, tags=None, state=None, attempt=None, created=None, modified=None, config=None, request=None, saved_files=None, produced_metadata=None):  # noqa: E501
        """Job - a model defined in Swagger"""

        self._id = None
        self._origin = None
        self._gear_id = None
        self._gear_info = None
        self._previous_job_id = None
        self._inputs = None
        self._destination = None
        self._tags = None
        self._state = None
        self._attempt = None
        self._created = None
        self._modified = None
        self._config = None
        self._request = None
        self._saved_files = None
        self._produced_metadata = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if origin is not None:
            self.origin = origin
        if gear_id is not None:
            self.gear_id = gear_id
        if gear_info is not None:
            self.gear_info = gear_info
        if previous_job_id is not None:
            self.previous_job_id = previous_job_id
        if inputs is not None:
            self.inputs = inputs
        if destination is not None:
            self.destination = destination
        if tags is not None:
            self.tags = tags
        if state is not None:
            self.state = state
        if attempt is not None:
            self.attempt = attempt
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if config is not None:
            self.config = config
        if request is not None:
            self.request = request
        if saved_files is not None:
            self.saved_files = saved_files
        if produced_metadata is not None:
            self.produced_metadata = produced_metadata

    @property
    def id(self):
        """Gets the id of this Job.

        Unique database ID

        :return: The id of this Job.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Job.

        Unique database ID

        :param id: The id of this Job.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def origin(self):
        """Gets the origin of this Job.


        :return: The origin of this Job.
        :rtype: JobOrigin
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this Job.


        :param origin: The origin of this Job.  # noqa: E501
        :type: JobOrigin
        """

        self._origin = origin

    @property
    def gear_id(self):
        """Gets the gear_id of this Job.


        :return: The gear_id of this Job.
        :rtype: str
        """
        return self._gear_id

    @gear_id.setter
    def gear_id(self, gear_id):
        """Sets the gear_id of this Job.


        :param gear_id: The gear_id of this Job.  # noqa: E501
        :type: str
        """

        self._gear_id = gear_id

    @property
    def gear_info(self):
        """Gets the gear_info of this Job.


        :return: The gear_info of this Job.
        :rtype: GearInfo
        """
        return self._gear_info

    @gear_info.setter
    def gear_info(self, gear_info):
        """Sets the gear_info of this Job.


        :param gear_info: The gear_info of this Job.  # noqa: E501
        :type: GearInfo
        """

        self._gear_info = gear_info

    @property
    def previous_job_id(self):
        """Gets the previous_job_id of this Job.


        :return: The previous_job_id of this Job.
        :rtype: str
        """
        return self._previous_job_id

    @previous_job_id.setter
    def previous_job_id(self, previous_job_id):
        """Sets the previous_job_id of this Job.


        :param previous_job_id: The previous_job_id of this Job.  # noqa: E501
        :type: str
        """

        self._previous_job_id = previous_job_id

    @property
    def inputs(self):
        """Gets the inputs of this Job.


        :return: The inputs of this Job.
        :rtype: JobInputsObject
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this Job.


        :param inputs: The inputs of this Job.  # noqa: E501
        :type: JobInputsObject
        """

        self._inputs = inputs

    @property
    def destination(self):
        """Gets the destination of this Job.


        :return: The destination of this Job.
        :rtype: JobDestination
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this Job.


        :param destination: The destination of this Job.  # noqa: E501
        :type: JobDestination
        """

        self._destination = destination

    @property
    def tags(self):
        """Gets the tags of this Job.


        :return: The tags of this Job.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this Job.


        :param tags: The tags of this Job.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def state(self):
        """Gets the state of this Job.


        :return: The state of this Job.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Job.


        :param state: The state of this Job.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def attempt(self):
        """Gets the attempt of this Job.


        :return: The attempt of this Job.
        :rtype: int
        """
        return self._attempt

    @attempt.setter
    def attempt(self, attempt):
        """Sets the attempt of this Job.


        :param attempt: The attempt of this Job.  # noqa: E501
        :type: int
        """

        self._attempt = attempt

    @property
    def created(self):
        """Gets the created of this Job.

        Creation time (automatically set)

        :return: The created of this Job.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Job.

        Creation time (automatically set)

        :param created: The created of this Job.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this Job.

        Last modification time (automatically updated)

        :return: The modified of this Job.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this Job.

        Last modification time (automatically updated)

        :param modified: The modified of this Job.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def config(self):
        """Gets the config of this Job.


        :return: The config of this Job.
        :rtype: JobConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this Job.


        :param config: The config of this Job.  # noqa: E501
        :type: JobConfig
        """

        self._config = config

    @property
    def request(self):
        """Gets the request of this Job.


        :return: The request of this Job.
        :rtype: JobRequest
        """
        return self._request

    @request.setter
    def request(self, request):
        """Sets the request of this Job.


        :param request: The request of this Job.  # noqa: E501
        :type: JobRequest
        """

        self._request = request

    @property
    def saved_files(self):
        """Gets the saved_files of this Job.


        :return: The saved_files of this Job.
        :rtype: list[str]
        """
        return self._saved_files

    @saved_files.setter
    def saved_files(self, saved_files):
        """Sets the saved_files of this Job.


        :param saved_files: The saved_files of this Job.  # noqa: E501
        :type: list[str]
        """

        self._saved_files = saved_files

    @property
    def produced_metadata(self):
        """Gets the produced_metadata of this Job.


        :return: The produced_metadata of this Job.
        :rtype: JobProducedMetadata
        """
        return self._produced_metadata

    @produced_metadata.setter
    def produced_metadata(self, produced_metadata):
        """Sets the produced_metadata of this Job.


        :param produced_metadata: The produced_metadata of this Job.  # noqa: E501
        :type: JobProducedMetadata
        """

        self._produced_metadata = produced_metadata


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
        if not isinstance(other, Job):
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
