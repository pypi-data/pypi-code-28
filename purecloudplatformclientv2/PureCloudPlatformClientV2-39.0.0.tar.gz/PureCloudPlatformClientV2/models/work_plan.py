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


class WorkPlan(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WorkPlan - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'enabled': 'bool',
            'constrain_weekly_paid_time': 'bool',
            'flexible_weekly_paid_time': 'bool',
            'weekly_exact_paid_minutes': 'int',
            'weekly_minimum_paid_minutes': 'int',
            'weekly_maximum_paid_minutes': 'int',
            'constrain_minimum_time_between_shifts': 'bool',
            'minimum_time_between_shifts_minutes': 'int',
            'maximum_days': 'int',
            'optional_days': 'SetWrapperDayOfWeek',
            'shift_start_variances': 'ListWrapperShiftStartVariance',
            'shifts': 'list[WorkPlanShift]',
            'agents': 'list[DeletableUserReference]',
            'metadata': 'WfmVersionedEntityMetadata',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'enabled': 'enabled',
            'constrain_weekly_paid_time': 'constrainWeeklyPaidTime',
            'flexible_weekly_paid_time': 'flexibleWeeklyPaidTime',
            'weekly_exact_paid_minutes': 'weeklyExactPaidMinutes',
            'weekly_minimum_paid_minutes': 'weeklyMinimumPaidMinutes',
            'weekly_maximum_paid_minutes': 'weeklyMaximumPaidMinutes',
            'constrain_minimum_time_between_shifts': 'constrainMinimumTimeBetweenShifts',
            'minimum_time_between_shifts_minutes': 'minimumTimeBetweenShiftsMinutes',
            'maximum_days': 'maximumDays',
            'optional_days': 'optionalDays',
            'shift_start_variances': 'shiftStartVariances',
            'shifts': 'shifts',
            'agents': 'agents',
            'metadata': 'metadata',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._enabled = None
        self._constrain_weekly_paid_time = None
        self._flexible_weekly_paid_time = None
        self._weekly_exact_paid_minutes = None
        self._weekly_minimum_paid_minutes = None
        self._weekly_maximum_paid_minutes = None
        self._constrain_minimum_time_between_shifts = None
        self._minimum_time_between_shifts_minutes = None
        self._maximum_days = None
        self._optional_days = None
        self._shift_start_variances = None
        self._shifts = None
        self._agents = None
        self._metadata = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this WorkPlan.
        The globally unique identifier for the object.

        :return: The id of this WorkPlan.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkPlan.
        The globally unique identifier for the object.

        :param id: The id of this WorkPlan.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this WorkPlan.


        :return: The name of this WorkPlan.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WorkPlan.


        :param name: The name of this WorkPlan.
        :type: str
        """
        
        self._name = name

    @property
    def enabled(self):
        """
        Gets the enabled of this WorkPlan.
        Whether the work plan is enabled for scheduling

        :return: The enabled of this WorkPlan.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this WorkPlan.
        Whether the work plan is enabled for scheduling

        :param enabled: The enabled of this WorkPlan.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def constrain_weekly_paid_time(self):
        """
        Gets the constrain_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is enabled for this work plan

        :return: The constrain_weekly_paid_time of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_weekly_paid_time

    @constrain_weekly_paid_time.setter
    def constrain_weekly_paid_time(self, constrain_weekly_paid_time):
        """
        Sets the constrain_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is enabled for this work plan

        :param constrain_weekly_paid_time: The constrain_weekly_paid_time of this WorkPlan.
        :type: bool
        """
        
        self._constrain_weekly_paid_time = constrain_weekly_paid_time

    @property
    def flexible_weekly_paid_time(self):
        """
        Gets the flexible_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is flexible for this work plan

        :return: The flexible_weekly_paid_time of this WorkPlan.
        :rtype: bool
        """
        return self._flexible_weekly_paid_time

    @flexible_weekly_paid_time.setter
    def flexible_weekly_paid_time(self, flexible_weekly_paid_time):
        """
        Sets the flexible_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is flexible for this work plan

        :param flexible_weekly_paid_time: The flexible_weekly_paid_time of this WorkPlan.
        :type: bool
        """
        
        self._flexible_weekly_paid_time = flexible_weekly_paid_time

    @property
    def weekly_exact_paid_minutes(self):
        """
        Gets the weekly_exact_paid_minutes of this WorkPlan.
        Exact weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == false

        :return: The weekly_exact_paid_minutes of this WorkPlan.
        :rtype: int
        """
        return self._weekly_exact_paid_minutes

    @weekly_exact_paid_minutes.setter
    def weekly_exact_paid_minutes(self, weekly_exact_paid_minutes):
        """
        Sets the weekly_exact_paid_minutes of this WorkPlan.
        Exact weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == false

        :param weekly_exact_paid_minutes: The weekly_exact_paid_minutes of this WorkPlan.
        :type: int
        """
        
        self._weekly_exact_paid_minutes = weekly_exact_paid_minutes

    @property
    def weekly_minimum_paid_minutes(self):
        """
        Gets the weekly_minimum_paid_minutes of this WorkPlan.
        Minimum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :return: The weekly_minimum_paid_minutes of this WorkPlan.
        :rtype: int
        """
        return self._weekly_minimum_paid_minutes

    @weekly_minimum_paid_minutes.setter
    def weekly_minimum_paid_minutes(self, weekly_minimum_paid_minutes):
        """
        Sets the weekly_minimum_paid_minutes of this WorkPlan.
        Minimum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :param weekly_minimum_paid_minutes: The weekly_minimum_paid_minutes of this WorkPlan.
        :type: int
        """
        
        self._weekly_minimum_paid_minutes = weekly_minimum_paid_minutes

    @property
    def weekly_maximum_paid_minutes(self):
        """
        Gets the weekly_maximum_paid_minutes of this WorkPlan.
        Maximum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :return: The weekly_maximum_paid_minutes of this WorkPlan.
        :rtype: int
        """
        return self._weekly_maximum_paid_minutes

    @weekly_maximum_paid_minutes.setter
    def weekly_maximum_paid_minutes(self, weekly_maximum_paid_minutes):
        """
        Sets the weekly_maximum_paid_minutes of this WorkPlan.
        Maximum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :param weekly_maximum_paid_minutes: The weekly_maximum_paid_minutes of this WorkPlan.
        :type: int
        """
        
        self._weekly_maximum_paid_minutes = weekly_maximum_paid_minutes

    @property
    def constrain_minimum_time_between_shifts(self):
        """
        Gets the constrain_minimum_time_between_shifts of this WorkPlan.
        Whether the minimum time between shifts constraint is enabled for this work plan

        :return: The constrain_minimum_time_between_shifts of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_minimum_time_between_shifts

    @constrain_minimum_time_between_shifts.setter
    def constrain_minimum_time_between_shifts(self, constrain_minimum_time_between_shifts):
        """
        Sets the constrain_minimum_time_between_shifts of this WorkPlan.
        Whether the minimum time between shifts constraint is enabled for this work plan

        :param constrain_minimum_time_between_shifts: The constrain_minimum_time_between_shifts of this WorkPlan.
        :type: bool
        """
        
        self._constrain_minimum_time_between_shifts = constrain_minimum_time_between_shifts

    @property
    def minimum_time_between_shifts_minutes(self):
        """
        Gets the minimum_time_between_shifts_minutes of this WorkPlan.
        Minimum time between shifts in minutes defined in this work plan. Used if constrainMinimumTimeBetweenShifts == true

        :return: The minimum_time_between_shifts_minutes of this WorkPlan.
        :rtype: int
        """
        return self._minimum_time_between_shifts_minutes

    @minimum_time_between_shifts_minutes.setter
    def minimum_time_between_shifts_minutes(self, minimum_time_between_shifts_minutes):
        """
        Sets the minimum_time_between_shifts_minutes of this WorkPlan.
        Minimum time between shifts in minutes defined in this work plan. Used if constrainMinimumTimeBetweenShifts == true

        :param minimum_time_between_shifts_minutes: The minimum_time_between_shifts_minutes of this WorkPlan.
        :type: int
        """
        
        self._minimum_time_between_shifts_minutes = minimum_time_between_shifts_minutes

    @property
    def maximum_days(self):
        """
        Gets the maximum_days of this WorkPlan.
        Maximum number days in a week allowed to be scheduled for this work plan

        :return: The maximum_days of this WorkPlan.
        :rtype: int
        """
        return self._maximum_days

    @maximum_days.setter
    def maximum_days(self, maximum_days):
        """
        Sets the maximum_days of this WorkPlan.
        Maximum number days in a week allowed to be scheduled for this work plan

        :param maximum_days: The maximum_days of this WorkPlan.
        :type: int
        """
        
        self._maximum_days = maximum_days

    @property
    def optional_days(self):
        """
        Gets the optional_days of this WorkPlan.
        Optional days to schedule for this work plan

        :return: The optional_days of this WorkPlan.
        :rtype: SetWrapperDayOfWeek
        """
        return self._optional_days

    @optional_days.setter
    def optional_days(self, optional_days):
        """
        Sets the optional_days of this WorkPlan.
        Optional days to schedule for this work plan

        :param optional_days: The optional_days of this WorkPlan.
        :type: SetWrapperDayOfWeek
        """
        
        self._optional_days = optional_days

    @property
    def shift_start_variances(self):
        """
        Gets the shift_start_variances of this WorkPlan.
        Variance in minutes among start times of shifts in this work plan

        :return: The shift_start_variances of this WorkPlan.
        :rtype: ListWrapperShiftStartVariance
        """
        return self._shift_start_variances

    @shift_start_variances.setter
    def shift_start_variances(self, shift_start_variances):
        """
        Sets the shift_start_variances of this WorkPlan.
        Variance in minutes among start times of shifts in this work plan

        :param shift_start_variances: The shift_start_variances of this WorkPlan.
        :type: ListWrapperShiftStartVariance
        """
        
        self._shift_start_variances = shift_start_variances

    @property
    def shifts(self):
        """
        Gets the shifts of this WorkPlan.
        Shifts in this work plan

        :return: The shifts of this WorkPlan.
        :rtype: list[WorkPlanShift]
        """
        return self._shifts

    @shifts.setter
    def shifts(self, shifts):
        """
        Sets the shifts of this WorkPlan.
        Shifts in this work plan

        :param shifts: The shifts of this WorkPlan.
        :type: list[WorkPlanShift]
        """
        
        self._shifts = shifts

    @property
    def agents(self):
        """
        Gets the agents of this WorkPlan.
        Agents in this work plan

        :return: The agents of this WorkPlan.
        :rtype: list[DeletableUserReference]
        """
        return self._agents

    @agents.setter
    def agents(self, agents):
        """
        Sets the agents of this WorkPlan.
        Agents in this work plan

        :param agents: The agents of this WorkPlan.
        :type: list[DeletableUserReference]
        """
        
        self._agents = agents

    @property
    def metadata(self):
        """
        Gets the metadata of this WorkPlan.
        Version metadata for this work plan

        :return: The metadata of this WorkPlan.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this WorkPlan.
        Version metadata for this work plan

        :param metadata: The metadata of this WorkPlan.
        :type: WfmVersionedEntityMetadata
        """
        
        self._metadata = metadata

    @property
    def self_uri(self):
        """
        Gets the self_uri of this WorkPlan.
        The URI for this object

        :return: The self_uri of this WorkPlan.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this WorkPlan.
        The URI for this object

        :param self_uri: The self_uri of this WorkPlan.
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

