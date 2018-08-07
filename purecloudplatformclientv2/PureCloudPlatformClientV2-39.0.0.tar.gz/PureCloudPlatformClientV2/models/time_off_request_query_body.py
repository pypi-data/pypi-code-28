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


class TimeOffRequestQueryBody(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TimeOffRequestQueryBody - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user_ids': 'list[str]',
            'statuses': 'list[str]',
            'date_range': 'DateRange'
        }

        self.attribute_map = {
            'user_ids': 'userIds',
            'statuses': 'statuses',
            'date_range': 'dateRange'
        }

        self._user_ids = None
        self._statuses = None
        self._date_range = None

    @property
    def user_ids(self):
        """
        Gets the user_ids of this TimeOffRequestQueryBody.
        The set of user ids to filter time off requests

        :return: The user_ids of this TimeOffRequestQueryBody.
        :rtype: list[str]
        """
        return self._user_ids

    @user_ids.setter
    def user_ids(self, user_ids):
        """
        Sets the user_ids of this TimeOffRequestQueryBody.
        The set of user ids to filter time off requests

        :param user_ids: The user_ids of this TimeOffRequestQueryBody.
        :type: list[str]
        """
        
        self._user_ids = user_ids

    @property
    def statuses(self):
        """
        Gets the statuses of this TimeOffRequestQueryBody.
        The set of statuses to filter time off requests

        :return: The statuses of this TimeOffRequestQueryBody.
        :rtype: list[str]
        """
        return self._statuses

    @statuses.setter
    def statuses(self, statuses):
        """
        Sets the statuses of this TimeOffRequestQueryBody.
        The set of statuses to filter time off requests

        :param statuses: The statuses of this TimeOffRequestQueryBody.
        :type: list[str]
        """
        
        self._statuses = statuses

    @property
    def date_range(self):
        """
        Gets the date_range of this TimeOffRequestQueryBody.
        The inclusive range of dates to filter time off requests

        :return: The date_range of this TimeOffRequestQueryBody.
        :rtype: DateRange
        """
        return self._date_range

    @date_range.setter
    def date_range(self, date_range):
        """
        Sets the date_range of this TimeOffRequestQueryBody.
        The inclusive range of dates to filter time off requests

        :param date_range: The date_range of this TimeOffRequestQueryBody.
        :type: DateRange
        """
        
        self._date_range = date_range

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

