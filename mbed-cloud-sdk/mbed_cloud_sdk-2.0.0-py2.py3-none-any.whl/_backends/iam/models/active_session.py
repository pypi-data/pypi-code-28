# coding: utf-8

"""
    Account Management API

    API for managing accounts, users, creating API keys, uploading trusted certificates

    OpenAPI spec version: v3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ActiveSession(object):
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
        'account_id': 'str',
        'ip_address': 'str',
        'login_time': 'datetime',
        'object': 'str',
        'reference_token': 'str',
        'user_agent': 'str'
    }

    attribute_map = {
        'account_id': 'account_id',
        'ip_address': 'ip_address',
        'login_time': 'login_time',
        'object': 'object',
        'reference_token': 'reference_token',
        'user_agent': 'user_agent'
    }

    def __init__(self, account_id=None, ip_address=None, login_time=None, object=None, reference_token=None, user_agent=None):
        """
        ActiveSession - a model defined in Swagger
        """

        self._account_id = account_id
        self._ip_address = ip_address
        self._login_time = login_time
        self._object = object
        self._reference_token = reference_token
        self._user_agent = user_agent
        self.discriminator = None

    @property
    def account_id(self):
        """
        Gets the account_id of this ActiveSession.
        The UUID of the account.

        :return: The account_id of this ActiveSession.
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this ActiveSession.
        The UUID of the account.

        :param account_id: The account_id of this ActiveSession.
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")

        self._account_id = account_id

    @property
    def ip_address(self):
        """
        Gets the ip_address of this ActiveSession.
        IP address of the client.

        :return: The ip_address of this ActiveSession.
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """
        Sets the ip_address of this ActiveSession.
        IP address of the client.

        :param ip_address: The ip_address of this ActiveSession.
        :type: str
        """
        if ip_address is None:
            raise ValueError("Invalid value for `ip_address`, must not be `None`")

        self._ip_address = ip_address

    @property
    def login_time(self):
        """
        Gets the login_time of this ActiveSession.
        The login time of the user.

        :return: The login_time of this ActiveSession.
        :rtype: datetime
        """
        return self._login_time

    @login_time.setter
    def login_time(self, login_time):
        """
        Sets the login_time of this ActiveSession.
        The login time of the user.

        :param login_time: The login_time of this ActiveSession.
        :type: datetime
        """
        if login_time is None:
            raise ValueError("Invalid value for `login_time`, must not be `None`")

        self._login_time = login_time

    @property
    def object(self):
        """
        Gets the object of this ActiveSession.
        Entity name: always 'user-session'

        :return: The object of this ActiveSession.
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this ActiveSession.
        Entity name: always 'user-session'

        :param object: The object of this ActiveSession.
        :type: str
        """
        if object is None:
            raise ValueError("Invalid value for `object`, must not be `None`")
        allowed_values = ["user-session"]
        if object not in allowed_values:
            raise ValueError(
                "Invalid value for `object` ({0}), must be one of {1}"
                .format(object, allowed_values)
            )

        self._object = object

    @property
    def reference_token(self):
        """
        Gets the reference_token of this ActiveSession.
        The reference token.

        :return: The reference_token of this ActiveSession.
        :rtype: str
        """
        return self._reference_token

    @reference_token.setter
    def reference_token(self, reference_token):
        """
        Sets the reference_token of this ActiveSession.
        The reference token.

        :param reference_token: The reference_token of this ActiveSession.
        :type: str
        """
        if reference_token is None:
            raise ValueError("Invalid value for `reference_token`, must not be `None`")

        self._reference_token = reference_token

    @property
    def user_agent(self):
        """
        Gets the user_agent of this ActiveSession.
        User Agent header from the login request.

        :return: The user_agent of this ActiveSession.
        :rtype: str
        """
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        """
        Sets the user_agent of this ActiveSession.
        User Agent header from the login request.

        :param user_agent: The user_agent of this ActiveSession.
        :type: str
        """
        if user_agent is None:
            raise ValueError("Invalid value for `user_agent`, must not be `None`")

        self._user_agent = user_agent

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
        if not isinstance(other, ActiveSession):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
