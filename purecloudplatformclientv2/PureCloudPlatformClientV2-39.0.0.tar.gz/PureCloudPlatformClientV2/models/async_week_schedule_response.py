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


class AsyncWeekScheduleResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AsyncWeekScheduleResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'status': 'str',
            'result': 'WeekSchedule',
            'operation_id': 'str',
            'download_url': 'str'
        }

        self.attribute_map = {
            'status': 'status',
            'result': 'result',
            'operation_id': 'operationId',
            'download_url': 'downloadUrl'
        }

        self._status = None
        self._result = None
        self._operation_id = None
        self._download_url = None

    @property
    def status(self):
        """
        Gets the status of this AsyncWeekScheduleResponse.
        The status of the request

        :return: The status of this AsyncWeekScheduleResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AsyncWeekScheduleResponse.
        The status of the request

        :param status: The status of this AsyncWeekScheduleResponse.
        :type: str
        """
        allowed_values = ["Processing", "Complete", "Error"]
        if status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for status -> " + status
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def result(self):
        """
        Gets the result of this AsyncWeekScheduleResponse.
        Week schedule result. The value will be null if the data is sent through notification or if response is large.

        :return: The result of this AsyncWeekScheduleResponse.
        :rtype: WeekSchedule
        """
        return self._result

    @result.setter
    def result(self, result):
        """
        Sets the result of this AsyncWeekScheduleResponse.
        Week schedule result. The value will be null if the data is sent through notification or if response is large.

        :param result: The result of this AsyncWeekScheduleResponse.
        :type: WeekSchedule
        """
        
        self._result = result

    @property
    def operation_id(self):
        """
        Gets the operation_id of this AsyncWeekScheduleResponse.
        The operation id to watch for on the notification topic if status == Processing

        :return: The operation_id of this AsyncWeekScheduleResponse.
        :rtype: str
        """
        return self._operation_id

    @operation_id.setter
    def operation_id(self, operation_id):
        """
        Sets the operation_id of this AsyncWeekScheduleResponse.
        The operation id to watch for on the notification topic if status == Processing

        :param operation_id: The operation_id of this AsyncWeekScheduleResponse.
        :type: str
        """
        
        self._operation_id = operation_id

    @property
    def download_url(self):
        """
        Gets the download_url of this AsyncWeekScheduleResponse.
        The url to fetch the result for large responses. The value will be null if result contains the data

        :return: The download_url of this AsyncWeekScheduleResponse.
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """
        Sets the download_url of this AsyncWeekScheduleResponse.
        The url to fetch the result for large responses. The value will be null if result contains the data

        :param download_url: The download_url of this AsyncWeekScheduleResponse.
        :type: str
        """
        
        self._download_url = download_url

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

