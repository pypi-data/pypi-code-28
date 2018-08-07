# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class WorkPlanListItemResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WorkPlanListItemResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'agent_count': 'int',
            'weekly_minimum_paid_minutes': 'int',
            'weekly_maximum_paid_minutes': 'int',
            'maximum_days': 'int',
            'enabled': 'bool',
            'metadata': 'WfmVersionedEntityMetadata',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'agent_count': 'agentCount',
            'weekly_minimum_paid_minutes': 'weeklyMinimumPaidMinutes',
            'weekly_maximum_paid_minutes': 'weeklyMaximumPaidMinutes',
            'maximum_days': 'maximumDays',
            'enabled': 'enabled',
            'metadata': 'metadata',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._agent_count = None
        self._weekly_minimum_paid_minutes = None
        self._weekly_maximum_paid_minutes = None
        self._maximum_days = None
        self._enabled = None
        self._metadata = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this WorkPlanListItemResponse.
        The globally unique identifier for the object.

        :return: The id of this WorkPlanListItemResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkPlanListItemResponse.
        The globally unique identifier for the object.

        :param id: The id of this WorkPlanListItemResponse.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this WorkPlanListItemResponse.


        :return: The name of this WorkPlanListItemResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WorkPlanListItemResponse.


        :param name: The name of this WorkPlanListItemResponse.
        :type: str
        """
        
        self._name = name

    @property
    def agent_count(self):
        """
        Gets the agent_count of this WorkPlanListItemResponse.
        Number of agents in this work plan

        :return: The agent_count of this WorkPlanListItemResponse.
        :rtype: int
        """
        return self._agent_count

    @agent_count.setter
    def agent_count(self, agent_count):
        """
        Sets the agent_count of this WorkPlanListItemResponse.
        Number of agents in this work plan

        :param agent_count: The agent_count of this WorkPlanListItemResponse.
        :type: int
        """
        
        self._agent_count = agent_count

    @property
    def weekly_minimum_paid_minutes(self):
        """
        Gets the weekly_minimum_paid_minutes of this WorkPlanListItemResponse.
        Minimum weekly paid time in minutes defined in this work plan

        :return: The weekly_minimum_paid_minutes of this WorkPlanListItemResponse.
        :rtype: int
        """
        return self._weekly_minimum_paid_minutes

    @weekly_minimum_paid_minutes.setter
    def weekly_minimum_paid_minutes(self, weekly_minimum_paid_minutes):
        """
        Sets the weekly_minimum_paid_minutes of this WorkPlanListItemResponse.
        Minimum weekly paid time in minutes defined in this work plan

        :param weekly_minimum_paid_minutes: The weekly_minimum_paid_minutes of this WorkPlanListItemResponse.
        :type: int
        """
        
        self._weekly_minimum_paid_minutes = weekly_minimum_paid_minutes

    @property
    def weekly_maximum_paid_minutes(self):
        """
        Gets the weekly_maximum_paid_minutes of this WorkPlanListItemResponse.
        Maximum weekly paid time in minutes defined in this work plan

        :return: The weekly_maximum_paid_minutes of this WorkPlanListItemResponse.
        :rtype: int
        """
        return self._weekly_maximum_paid_minutes

    @weekly_maximum_paid_minutes.setter
    def weekly_maximum_paid_minutes(self, weekly_maximum_paid_minutes):
        """
        Sets the weekly_maximum_paid_minutes of this WorkPlanListItemResponse.
        Maximum weekly paid time in minutes defined in this work plan

        :param weekly_maximum_paid_minutes: The weekly_maximum_paid_minutes of this WorkPlanListItemResponse.
        :type: int
        """
        
        self._weekly_maximum_paid_minutes = weekly_maximum_paid_minutes

    @property
    def maximum_days(self):
        """
        Gets the maximum_days of this WorkPlanListItemResponse.
        Maximum number of days in a week that can be scheduled using this work plan

        :return: The maximum_days of this WorkPlanListItemResponse.
        :rtype: int
        """
        return self._maximum_days

    @maximum_days.setter
    def maximum_days(self, maximum_days):
        """
        Sets the maximum_days of this WorkPlanListItemResponse.
        Maximum number of days in a week that can be scheduled using this work plan

        :param maximum_days: The maximum_days of this WorkPlanListItemResponse.
        :type: int
        """
        
        self._maximum_days = maximum_days

    @property
    def enabled(self):
        """
        Gets the enabled of this WorkPlanListItemResponse.
        Whether the work plan is enabled for scheduling

        :return: The enabled of this WorkPlanListItemResponse.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this WorkPlanListItemResponse.
        Whether the work plan is enabled for scheduling

        :param enabled: The enabled of this WorkPlanListItemResponse.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def metadata(self):
        """
        Gets the metadata of this WorkPlanListItemResponse.
        Version metadata for this work plan

        :return: The metadata of this WorkPlanListItemResponse.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this WorkPlanListItemResponse.
        Version metadata for this work plan

        :param metadata: The metadata of this WorkPlanListItemResponse.
        :type: WfmVersionedEntityMetadata
        """
        
        self._metadata = metadata

    @property
    def self_uri(self):
        """
        Gets the self_uri of this WorkPlanListItemResponse.
        The URI for this object

        :return: The self_uri of this WorkPlanListItemResponse.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this WorkPlanListItemResponse.
        The URI for this object

        :param self_uri: The self_uri of this WorkPlanListItemResponse.
        :type: str
        """
        
        self._self_uri = self_uri

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
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

