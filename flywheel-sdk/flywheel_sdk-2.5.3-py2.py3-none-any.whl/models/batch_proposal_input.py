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

from flywheel.models.analysis_input import AnalysisInput  # noqa: F401,E501
from flywheel.models.container_reference import ContainerReference  # noqa: F401,E501
from flywheel.models.job_config import JobConfig  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class BatchProposalInput(object):

    swagger_types = {
        'gear_id': 'str',
        'config': 'JobConfig',
        'tags': 'list[str]',
        'analysis': 'AnalysisInput',
        'targets': 'list[ContainerReference]'
    }

    attribute_map = {
        'gear_id': 'gear_id',
        'config': 'config',
        'tags': 'tags',
        'analysis': 'analysis',
        'targets': 'targets'
    }

    rattribute_map = {
        'gear_id': 'gear_id',
        'config': 'config',
        'tags': 'tags',
        'analysis': 'analysis',
        'targets': 'targets'
    }

    def __init__(self, gear_id=None, config=None, tags=None, analysis=None, targets=None):  # noqa: E501
        """BatchProposalInput - a model defined in Swagger"""

        self._gear_id = None
        self._config = None
        self._tags = None
        self._analysis = None
        self._targets = None
        self.discriminator = None
        self.alt_discriminator = None

        if gear_id is not None:
            self.gear_id = gear_id
        if config is not None:
            self.config = config
        if tags is not None:
            self.tags = tags
        if analysis is not None:
            self.analysis = analysis
        if targets is not None:
            self.targets = targets

    @property
    def gear_id(self):
        """Gets the gear_id of this BatchProposalInput.


        :return: The gear_id of this BatchProposalInput.
        :rtype: str
        """
        return self._gear_id

    @gear_id.setter
    def gear_id(self, gear_id):
        """Sets the gear_id of this BatchProposalInput.


        :param gear_id: The gear_id of this BatchProposalInput.  # noqa: E501
        :type: str
        """

        self._gear_id = gear_id

    @property
    def config(self):
        """Gets the config of this BatchProposalInput.


        :return: The config of this BatchProposalInput.
        :rtype: JobConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this BatchProposalInput.


        :param config: The config of this BatchProposalInput.  # noqa: E501
        :type: JobConfig
        """

        self._config = config

    @property
    def tags(self):
        """Gets the tags of this BatchProposalInput.

        Array of application-specific tags

        :return: The tags of this BatchProposalInput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this BatchProposalInput.

        Array of application-specific tags

        :param tags: The tags of this BatchProposalInput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def analysis(self):
        """Gets the analysis of this BatchProposalInput.


        :return: The analysis of this BatchProposalInput.
        :rtype: AnalysisInput
        """
        return self._analysis

    @analysis.setter
    def analysis(self, analysis):
        """Sets the analysis of this BatchProposalInput.


        :param analysis: The analysis of this BatchProposalInput.  # noqa: E501
        :type: AnalysisInput
        """

        self._analysis = analysis

    @property
    def targets(self):
        """Gets the targets of this BatchProposalInput.


        :return: The targets of this BatchProposalInput.
        :rtype: list[ContainerReference]
        """
        return self._targets

    @targets.setter
    def targets(self, targets):
        """Sets the targets of this BatchProposalInput.


        :param targets: The targets of this BatchProposalInput.  # noqa: E501
        :type: list[ContainerReference]
        """

        self._targets = targets


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
        if not isinstance(other, BatchProposalInput):
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
