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


class SocialConversationNotificationSocialMediaParticipant(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SocialConversationNotificationSocialMediaParticipant - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'address': 'str',
            'start_time': 'datetime',
            'connected_time': 'datetime',
            'end_time': 'datetime',
            'start_hold_time': 'datetime',
            'purpose': 'str',
            'state': 'str',
            'direction': 'str',
            'disconnect_type': 'str',
            'held': 'bool',
            'wrapup_required': 'bool',
            'wrapup_prompt': 'str',
            'user': 'DocumentDataV2NotificationCreatedBy',
            'queue': 'SocialConversationNotificationUriReference',
            'attributes': 'dict(str, str)',
            'error_info': 'SocialConversationNotificationErrorInfo',
            'script': 'SocialConversationNotificationUriReference',
            'wrapup_timeout_ms': 'int',
            'wrapup_skipped': 'bool',
            'provider': 'str',
            'external_contact': 'SocialConversationNotificationUriReference',
            'external_organization': 'SocialConversationNotificationUriReference',
            'wrapup': 'ConversationNotificationWrapup',
            'peer': 'str',
            'screen_recording_state': 'str',
            'flagged_reason': 'str',
            'social_media_id': 'str',
            'social_media_hub': 'str',
            'social_user_name': 'str',
            'preview_text': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'address': 'address',
            'start_time': 'startTime',
            'connected_time': 'connectedTime',
            'end_time': 'endTime',
            'start_hold_time': 'startHoldTime',
            'purpose': 'purpose',
            'state': 'state',
            'direction': 'direction',
            'disconnect_type': 'disconnectType',
            'held': 'held',
            'wrapup_required': 'wrapupRequired',
            'wrapup_prompt': 'wrapupPrompt',
            'user': 'user',
            'queue': 'queue',
            'attributes': 'attributes',
            'error_info': 'errorInfo',
            'script': 'script',
            'wrapup_timeout_ms': 'wrapupTimeoutMs',
            'wrapup_skipped': 'wrapupSkipped',
            'provider': 'provider',
            'external_contact': 'externalContact',
            'external_organization': 'externalOrganization',
            'wrapup': 'wrapup',
            'peer': 'peer',
            'screen_recording_state': 'screenRecordingState',
            'flagged_reason': 'flaggedReason',
            'social_media_id': 'socialMediaId',
            'social_media_hub': 'socialMediaHub',
            'social_user_name': 'socialUserName',
            'preview_text': 'previewText'
        }

        self._id = None
        self._name = None
        self._address = None
        self._start_time = None
        self._connected_time = None
        self._end_time = None
        self._start_hold_time = None
        self._purpose = None
        self._state = None
        self._direction = None
        self._disconnect_type = None
        self._held = None
        self._wrapup_required = None
        self._wrapup_prompt = None
        self._user = None
        self._queue = None
        self._attributes = None
        self._error_info = None
        self._script = None
        self._wrapup_timeout_ms = None
        self._wrapup_skipped = None
        self._provider = None
        self._external_contact = None
        self._external_organization = None
        self._wrapup = None
        self._peer = None
        self._screen_recording_state = None
        self._flagged_reason = None
        self._social_media_id = None
        self._social_media_hub = None
        self._social_user_name = None
        self._preview_text = None

    @property
    def id(self):
        """
        Gets the id of this SocialConversationNotificationSocialMediaParticipant.


        :return: The id of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SocialConversationNotificationSocialMediaParticipant.


        :param id: The id of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this SocialConversationNotificationSocialMediaParticipant.


        :return: The name of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SocialConversationNotificationSocialMediaParticipant.


        :param name: The name of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._name = name

    @property
    def address(self):
        """
        Gets the address of this SocialConversationNotificationSocialMediaParticipant.


        :return: The address of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets the address of this SocialConversationNotificationSocialMediaParticipant.


        :param address: The address of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._address = address

    @property
    def start_time(self):
        """
        Gets the start_time of this SocialConversationNotificationSocialMediaParticipant.


        :return: The start_time of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this SocialConversationNotificationSocialMediaParticipant.


        :param start_time: The start_time of this SocialConversationNotificationSocialMediaParticipant.
        :type: datetime
        """
        
        self._start_time = start_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this SocialConversationNotificationSocialMediaParticipant.


        :return: The connected_time of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this SocialConversationNotificationSocialMediaParticipant.


        :param connected_time: The connected_time of this SocialConversationNotificationSocialMediaParticipant.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def end_time(self):
        """
        Gets the end_time of this SocialConversationNotificationSocialMediaParticipant.


        :return: The end_time of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this SocialConversationNotificationSocialMediaParticipant.


        :param end_time: The end_time of this SocialConversationNotificationSocialMediaParticipant.
        :type: datetime
        """
        
        self._end_time = end_time

    @property
    def start_hold_time(self):
        """
        Gets the start_hold_time of this SocialConversationNotificationSocialMediaParticipant.


        :return: The start_hold_time of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: datetime
        """
        return self._start_hold_time

    @start_hold_time.setter
    def start_hold_time(self, start_hold_time):
        """
        Sets the start_hold_time of this SocialConversationNotificationSocialMediaParticipant.


        :param start_hold_time: The start_hold_time of this SocialConversationNotificationSocialMediaParticipant.
        :type: datetime
        """
        
        self._start_hold_time = start_hold_time

    @property
    def purpose(self):
        """
        Gets the purpose of this SocialConversationNotificationSocialMediaParticipant.


        :return: The purpose of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._purpose

    @purpose.setter
    def purpose(self, purpose):
        """
        Sets the purpose of this SocialConversationNotificationSocialMediaParticipant.


        :param purpose: The purpose of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._purpose = purpose

    @property
    def state(self):
        """
        Gets the state of this SocialConversationNotificationSocialMediaParticipant.


        :return: The state of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this SocialConversationNotificationSocialMediaParticipant.


        :param state: The state of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        allowed_values = ["alerting", "dialing", "contacting", "offering", "connected", "disconnected", "terminated", "converting", "uploading", "transmitting", "scheduled", "none"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def direction(self):
        """
        Gets the direction of this SocialConversationNotificationSocialMediaParticipant.


        :return: The direction of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this SocialConversationNotificationSocialMediaParticipant.


        :param direction: The direction of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        allowed_values = ["inbound", "outbound"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for direction -> " + direction
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this SocialConversationNotificationSocialMediaParticipant.


        :return: The disconnect_type of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this SocialConversationNotificationSocialMediaParticipant.


        :param disconnect_type: The disconnect_type of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        allowed_values = ["endpoint", "client", "system", "transfer", "timeout", "transfer.conference", "transfer.consult", "transfer.forward", "transfer.noanswer", "transfer.notavailable", "transport.failure", "error", "peer", "other", "spam", "uncallable"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for disconnect_type -> " + disconnect_type
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def held(self):
        """
        Gets the held of this SocialConversationNotificationSocialMediaParticipant.


        :return: The held of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: bool
        """
        return self._held

    @held.setter
    def held(self, held):
        """
        Sets the held of this SocialConversationNotificationSocialMediaParticipant.


        :param held: The held of this SocialConversationNotificationSocialMediaParticipant.
        :type: bool
        """
        
        self._held = held

    @property
    def wrapup_required(self):
        """
        Gets the wrapup_required of this SocialConversationNotificationSocialMediaParticipant.


        :return: The wrapup_required of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: bool
        """
        return self._wrapup_required

    @wrapup_required.setter
    def wrapup_required(self, wrapup_required):
        """
        Sets the wrapup_required of this SocialConversationNotificationSocialMediaParticipant.


        :param wrapup_required: The wrapup_required of this SocialConversationNotificationSocialMediaParticipant.
        :type: bool
        """
        
        self._wrapup_required = wrapup_required

    @property
    def wrapup_prompt(self):
        """
        Gets the wrapup_prompt of this SocialConversationNotificationSocialMediaParticipant.


        :return: The wrapup_prompt of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._wrapup_prompt

    @wrapup_prompt.setter
    def wrapup_prompt(self, wrapup_prompt):
        """
        Sets the wrapup_prompt of this SocialConversationNotificationSocialMediaParticipant.


        :param wrapup_prompt: The wrapup_prompt of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._wrapup_prompt = wrapup_prompt

    @property
    def user(self):
        """
        Gets the user of this SocialConversationNotificationSocialMediaParticipant.


        :return: The user of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: DocumentDataV2NotificationCreatedBy
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this SocialConversationNotificationSocialMediaParticipant.


        :param user: The user of this SocialConversationNotificationSocialMediaParticipant.
        :type: DocumentDataV2NotificationCreatedBy
        """
        
        self._user = user

    @property
    def queue(self):
        """
        Gets the queue of this SocialConversationNotificationSocialMediaParticipant.


        :return: The queue of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: SocialConversationNotificationUriReference
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """
        Sets the queue of this SocialConversationNotificationSocialMediaParticipant.


        :param queue: The queue of this SocialConversationNotificationSocialMediaParticipant.
        :type: SocialConversationNotificationUriReference
        """
        
        self._queue = queue

    @property
    def attributes(self):
        """
        Gets the attributes of this SocialConversationNotificationSocialMediaParticipant.


        :return: The attributes of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: dict(str, str)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this SocialConversationNotificationSocialMediaParticipant.


        :param attributes: The attributes of this SocialConversationNotificationSocialMediaParticipant.
        :type: dict(str, str)
        """
        
        self._attributes = attributes

    @property
    def error_info(self):
        """
        Gets the error_info of this SocialConversationNotificationSocialMediaParticipant.


        :return: The error_info of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: SocialConversationNotificationErrorInfo
        """
        return self._error_info

    @error_info.setter
    def error_info(self, error_info):
        """
        Sets the error_info of this SocialConversationNotificationSocialMediaParticipant.


        :param error_info: The error_info of this SocialConversationNotificationSocialMediaParticipant.
        :type: SocialConversationNotificationErrorInfo
        """
        
        self._error_info = error_info

    @property
    def script(self):
        """
        Gets the script of this SocialConversationNotificationSocialMediaParticipant.


        :return: The script of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: SocialConversationNotificationUriReference
        """
        return self._script

    @script.setter
    def script(self, script):
        """
        Sets the script of this SocialConversationNotificationSocialMediaParticipant.


        :param script: The script of this SocialConversationNotificationSocialMediaParticipant.
        :type: SocialConversationNotificationUriReference
        """
        
        self._script = script

    @property
    def wrapup_timeout_ms(self):
        """
        Gets the wrapup_timeout_ms of this SocialConversationNotificationSocialMediaParticipant.


        :return: The wrapup_timeout_ms of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: int
        """
        return self._wrapup_timeout_ms

    @wrapup_timeout_ms.setter
    def wrapup_timeout_ms(self, wrapup_timeout_ms):
        """
        Sets the wrapup_timeout_ms of this SocialConversationNotificationSocialMediaParticipant.


        :param wrapup_timeout_ms: The wrapup_timeout_ms of this SocialConversationNotificationSocialMediaParticipant.
        :type: int
        """
        
        self._wrapup_timeout_ms = wrapup_timeout_ms

    @property
    def wrapup_skipped(self):
        """
        Gets the wrapup_skipped of this SocialConversationNotificationSocialMediaParticipant.


        :return: The wrapup_skipped of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: bool
        """
        return self._wrapup_skipped

    @wrapup_skipped.setter
    def wrapup_skipped(self, wrapup_skipped):
        """
        Sets the wrapup_skipped of this SocialConversationNotificationSocialMediaParticipant.


        :param wrapup_skipped: The wrapup_skipped of this SocialConversationNotificationSocialMediaParticipant.
        :type: bool
        """
        
        self._wrapup_skipped = wrapup_skipped

    @property
    def provider(self):
        """
        Gets the provider of this SocialConversationNotificationSocialMediaParticipant.


        :return: The provider of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this SocialConversationNotificationSocialMediaParticipant.


        :param provider: The provider of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._provider = provider

    @property
    def external_contact(self):
        """
        Gets the external_contact of this SocialConversationNotificationSocialMediaParticipant.


        :return: The external_contact of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: SocialConversationNotificationUriReference
        """
        return self._external_contact

    @external_contact.setter
    def external_contact(self, external_contact):
        """
        Sets the external_contact of this SocialConversationNotificationSocialMediaParticipant.


        :param external_contact: The external_contact of this SocialConversationNotificationSocialMediaParticipant.
        :type: SocialConversationNotificationUriReference
        """
        
        self._external_contact = external_contact

    @property
    def external_organization(self):
        """
        Gets the external_organization of this SocialConversationNotificationSocialMediaParticipant.


        :return: The external_organization of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: SocialConversationNotificationUriReference
        """
        return self._external_organization

    @external_organization.setter
    def external_organization(self, external_organization):
        """
        Sets the external_organization of this SocialConversationNotificationSocialMediaParticipant.


        :param external_organization: The external_organization of this SocialConversationNotificationSocialMediaParticipant.
        :type: SocialConversationNotificationUriReference
        """
        
        self._external_organization = external_organization

    @property
    def wrapup(self):
        """
        Gets the wrapup of this SocialConversationNotificationSocialMediaParticipant.


        :return: The wrapup of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: ConversationNotificationWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this SocialConversationNotificationSocialMediaParticipant.


        :param wrapup: The wrapup of this SocialConversationNotificationSocialMediaParticipant.
        :type: ConversationNotificationWrapup
        """
        
        self._wrapup = wrapup

    @property
    def peer(self):
        """
        Gets the peer of this SocialConversationNotificationSocialMediaParticipant.


        :return: The peer of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._peer

    @peer.setter
    def peer(self, peer):
        """
        Sets the peer of this SocialConversationNotificationSocialMediaParticipant.


        :param peer: The peer of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._peer = peer

    @property
    def screen_recording_state(self):
        """
        Gets the screen_recording_state of this SocialConversationNotificationSocialMediaParticipant.


        :return: The screen_recording_state of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._screen_recording_state

    @screen_recording_state.setter
    def screen_recording_state(self, screen_recording_state):
        """
        Sets the screen_recording_state of this SocialConversationNotificationSocialMediaParticipant.


        :param screen_recording_state: The screen_recording_state of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._screen_recording_state = screen_recording_state

    @property
    def flagged_reason(self):
        """
        Gets the flagged_reason of this SocialConversationNotificationSocialMediaParticipant.


        :return: The flagged_reason of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._flagged_reason

    @flagged_reason.setter
    def flagged_reason(self, flagged_reason):
        """
        Sets the flagged_reason of this SocialConversationNotificationSocialMediaParticipant.


        :param flagged_reason: The flagged_reason of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        allowed_values = ["general"]
        if flagged_reason.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for flagged_reason -> " + flagged_reason
            self._flagged_reason = "outdated_sdk_version"
        else:
            self._flagged_reason = flagged_reason

    @property
    def social_media_id(self):
        """
        Gets the social_media_id of this SocialConversationNotificationSocialMediaParticipant.


        :return: The social_media_id of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._social_media_id

    @social_media_id.setter
    def social_media_id(self, social_media_id):
        """
        Sets the social_media_id of this SocialConversationNotificationSocialMediaParticipant.


        :param social_media_id: The social_media_id of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._social_media_id = social_media_id

    @property
    def social_media_hub(self):
        """
        Gets the social_media_hub of this SocialConversationNotificationSocialMediaParticipant.


        :return: The social_media_hub of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._social_media_hub

    @social_media_hub.setter
    def social_media_hub(self, social_media_hub):
        """
        Sets the social_media_hub of this SocialConversationNotificationSocialMediaParticipant.


        :param social_media_hub: The social_media_hub of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._social_media_hub = social_media_hub

    @property
    def social_user_name(self):
        """
        Gets the social_user_name of this SocialConversationNotificationSocialMediaParticipant.


        :return: The social_user_name of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._social_user_name

    @social_user_name.setter
    def social_user_name(self, social_user_name):
        """
        Sets the social_user_name of this SocialConversationNotificationSocialMediaParticipant.


        :param social_user_name: The social_user_name of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._social_user_name = social_user_name

    @property
    def preview_text(self):
        """
        Gets the preview_text of this SocialConversationNotificationSocialMediaParticipant.


        :return: The preview_text of this SocialConversationNotificationSocialMediaParticipant.
        :rtype: str
        """
        return self._preview_text

    @preview_text.setter
    def preview_text(self, preview_text):
        """
        Sets the preview_text of this SocialConversationNotificationSocialMediaParticipant.


        :param preview_text: The preview_text of this SocialConversationNotificationSocialMediaParticipant.
        :type: str
        """
        
        self._preview_text = preview_text

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

