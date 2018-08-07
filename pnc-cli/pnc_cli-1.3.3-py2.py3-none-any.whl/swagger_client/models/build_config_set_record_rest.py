# coding: utf-8

"""
Copyright 2015 SmartBear Software

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

from datetime import datetime
from pprint import pformat
from six import iteritems


class BuildConfigSetRecordRest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuildConfigSetRecordRest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'build_configuration_set_id': 'int',
            'build_configuration_set_name': 'str',
            'start_time': 'datetime',
            'end_time': 'datetime',
            'status': 'str',
            'user_id': 'int',
            'username': 'str',
            'product_version_id': 'int',
            'build_record_ids': 'list[int]',
            'temporary_build': 'bool'
        }

        self.attribute_map = {
            'id': 'id',
            'build_configuration_set_id': 'buildConfigurationSetId',
            'build_configuration_set_name': 'buildConfigurationSetName',
            'start_time': 'startTime',
            'end_time': 'endTime',
            'status': 'status',
            'user_id': 'userId',
            'username': 'username',
            'product_version_id': 'productVersionId',
            'build_record_ids': 'buildRecordIds',
            'temporary_build': 'temporaryBuild'
        }

        self._id = None
        self._build_configuration_set_id = None
        self._build_configuration_set_name = None
        self._start_time = None
        self._end_time = None
        self._status = None
        self._user_id = None
        self._username = None
        self._product_version_id = None
        self._build_record_ids = None
        self._temporary_build = None

    @property
    def id(self):
        """
        Gets the id of this BuildConfigSetRecordRest.


        :return: The id of this BuildConfigSetRecordRest.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BuildConfigSetRecordRest.


        :param id: The id of this BuildConfigSetRecordRest.
        :type: int
        """
        self._id = id

    @property
    def build_configuration_set_id(self):
        """
        Gets the build_configuration_set_id of this BuildConfigSetRecordRest.


        :return: The build_configuration_set_id of this BuildConfigSetRecordRest.
        :rtype: int
        """
        return self._build_configuration_set_id

    @build_configuration_set_id.setter
    def build_configuration_set_id(self, build_configuration_set_id):
        """
        Sets the build_configuration_set_id of this BuildConfigSetRecordRest.


        :param build_configuration_set_id: The build_configuration_set_id of this BuildConfigSetRecordRest.
        :type: int
        """
        self._build_configuration_set_id = build_configuration_set_id

    @property
    def build_configuration_set_name(self):
        """
        Gets the build_configuration_set_name of this BuildConfigSetRecordRest.


        :return: The build_configuration_set_name of this BuildConfigSetRecordRest.
        :rtype: str
        """
        return self._build_configuration_set_name

    @build_configuration_set_name.setter
    def build_configuration_set_name(self, build_configuration_set_name):
        """
        Sets the build_configuration_set_name of this BuildConfigSetRecordRest.


        :param build_configuration_set_name: The build_configuration_set_name of this BuildConfigSetRecordRest.
        :type: str
        """
        self._build_configuration_set_name = build_configuration_set_name

    @property
    def start_time(self):
        """
        Gets the start_time of this BuildConfigSetRecordRest.


        :return: The start_time of this BuildConfigSetRecordRest.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this BuildConfigSetRecordRest.


        :param start_time: The start_time of this BuildConfigSetRecordRest.
        :type: datetime
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """
        Gets the end_time of this BuildConfigSetRecordRest.


        :return: The end_time of this BuildConfigSetRecordRest.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this BuildConfigSetRecordRest.


        :param end_time: The end_time of this BuildConfigSetRecordRest.
        :type: datetime
        """
        self._end_time = end_time

    @property
    def status(self):
        """
        Gets the status of this BuildConfigSetRecordRest.


        :return: The status of this BuildConfigSetRecordRest.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this BuildConfigSetRecordRest.


        :param status: The status of this BuildConfigSetRecordRest.
        :type: str
        """
        allowed_values = ["SUCCESS", "FAILED", "UNSTABLE", "BUILDING", "REJECTED", "CANCELLED", "SYSTEM_ERROR", "UNKNOWN", "NONE"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status`, must be one of {0}"
                .format(allowed_values)
            )
        self._status = status

    @property
    def user_id(self):
        """
        Gets the user_id of this BuildConfigSetRecordRest.


        :return: The user_id of this BuildConfigSetRecordRest.
        :rtype: int
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this BuildConfigSetRecordRest.


        :param user_id: The user_id of this BuildConfigSetRecordRest.
        :type: int
        """
        self._user_id = user_id

    @property
    def username(self):
        """
        Gets the username of this BuildConfigSetRecordRest.


        :return: The username of this BuildConfigSetRecordRest.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this BuildConfigSetRecordRest.


        :param username: The username of this BuildConfigSetRecordRest.
        :type: str
        """
        self._username = username

    @property
    def product_version_id(self):
        """
        Gets the product_version_id of this BuildConfigSetRecordRest.


        :return: The product_version_id of this BuildConfigSetRecordRest.
        :rtype: int
        """
        return self._product_version_id

    @product_version_id.setter
    def product_version_id(self, product_version_id):
        """
        Sets the product_version_id of this BuildConfigSetRecordRest.


        :param product_version_id: The product_version_id of this BuildConfigSetRecordRest.
        :type: int
        """
        self._product_version_id = product_version_id

    @property
    def build_record_ids(self):
        """
        Gets the build_record_ids of this BuildConfigSetRecordRest.


        :return: The build_record_ids of this BuildConfigSetRecordRest.
        :rtype: list[int]
        """
        return self._build_record_ids

    @build_record_ids.setter
    def build_record_ids(self, build_record_ids):
        """
        Sets the build_record_ids of this BuildConfigSetRecordRest.


        :param build_record_ids: The build_record_ids of this BuildConfigSetRecordRest.
        :type: list[int]
        """
        self._build_record_ids = build_record_ids

    @property
    def temporary_build(self):
        """
        Gets the temporary_build of this BuildConfigSetRecordRest.


        :return: The temporary_build of this BuildConfigSetRecordRest.
        :rtype: bool
        """
        return self._temporary_build

    @temporary_build.setter
    def temporary_build(self, temporary_build):
        """
        Sets the temporary_build of this BuildConfigSetRecordRest.


        :param temporary_build: The temporary_build of this BuildConfigSetRecordRest.
        :type: bool
        """
        self._temporary_build = temporary_build

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
	    elif isinstance(value, datetime):
		result[attr] = str(value.date())
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
