"""On/Off states."""
import asyncio

from insteonplm.constants import (COMMAND_LIGHT_MANUALLY_TURNED_ON_0X23_0X00,
                                  COMMAND_LIGHT_MANUALLY_TURNED_OFF_0X22_0X00,
                                  COMMAND_LIGHT_OFF_0X13_0X00,
                                  COMMAND_LIGHT_OFF_FAST_0X14_0X00,
                                  COMMAND_LIGHT_ON_0X11_NONE,
                                  COMMAND_LIGHT_ON_FAST_0X12_NONE,
                                  COMMAND_LIGHT_STATUS_REQUEST_0X19_0X00,
                                  COMMAND_LIGHT_STATUS_REQUEST_0X19_0X01,
                                  MESSAGE_TYPE_ALL_LINK_BROADCAST,
                                  MESSAGE_TYPE_ALL_LINK_CLEANUP,
                                  MESSAGE_TYPE_DIRECT_MESSAGE,
                                  COMMAND_EXTENDED_TRIGGER_ALL_LINK_0X30_0X00,
                                  COMMAND_EXTENDED_GET_SET_0X2E_0X00)
from insteonplm.messages.standardSend import StandardSend
from insteonplm.messages.extendedSend import ExtendedSend
from insteonplm.messages.standardReceive import StandardReceive
from insteonplm.messages.extendedReceive import ExtendedReceive
from insteonplm.messages.messageFlags import MessageFlags
from insteonplm.messages.userdata import Userdata
from insteonplm.states import State
from insteonplm.utils import bit_is_set, set_bit


class OnOffStateBase(State):
    """Base state representing an On/Off switch that is controllable.

    Available properties are:
      value
      name
      address
      group

    Available methods are:
      register_updates()
      async_refresh_state()
    """

    def __init__(self, address, statename, group, send_message_method,
                 message_callbacks, defaultvalue=None):
        """Initialize the OnOffStateBase."""
        super().__init__(address, statename, group, send_message_method,
                         message_callbacks, defaultvalue)

        self._updatemethod = self._send_status_request

        self._register_messages()

    def _on_message_received(self, msg):
        """An ON has been received."""
        self._update_subscribers(0xff)

    def _off_message_received(self, msg):
        """An OFF has been received."""
        self._update_subscribers(0x00)

    def _manual_change_received(self, msg):
        """A manual change message has been received."""
        self._send_status_request()

    def _send_status_request(self):
        """Send a status request message to the device."""
        status_command = StandardSend(self._address,
                                      COMMAND_LIGHT_STATUS_REQUEST_0X19_0X00)
        self._send_method(status_command,
                          self._status_message_received)

    def _status_message_received(self, msg):
        """A status message has been received."""
        if msg.cmd2 == 0x00:
            self._update_subscribers(0x00)
        else:
            self._update_subscribers(0xff)

    def _register_messages(self):
        """Register messages to listen for."""
        template_on_group = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_ON_0X11_NONE,
            address=self._address,
            target=bytearray([0x00, 0x00, self._group]),
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_BROADCAST, None))
        template_fast_on_group = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_ON_FAST_0X12_NONE,
            address=self._address,
            target=bytearray([0x00, 0x00, self._group]),
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_BROADCAST, None))
        template_off_group = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_OFF_0X13_0X00,
            address=self._address,
            target=bytearray([0x00, 0x00, self._group]),
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_BROADCAST, None),
            cmd2=None)
        template_fast_off_group = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_OFF_FAST_0X14_0X00,
            address=self._address,
            target=bytearray([0x00, 0x00, self._group]),
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_BROADCAST, None),
            cmd2=None)
        template_manual_on_group = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_MANUALLY_TURNED_ON_0X23_0X00,
            address=self._address,
            target=bytearray([0x00, 0x00, self._group]),
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_BROADCAST, None),
            cmd2=None)
        template_manual_off_group = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_MANUALLY_TURNED_OFF_0X22_0X00,
            address=self._address,
            target=bytearray([0x00, 0x00, self._group]),
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_BROADCAST, None),
            cmd2=None)

        template_on_cleanup = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_ON_0X11_NONE,
            address=self._address,
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_CLEANUP, None),
            cmd2=self._group)
        template_fast_on_cleanup = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_ON_FAST_0X12_NONE,
            address=self._address,
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_CLEANUP, None),
            cmd2=self._group)
        template_off_cleanup = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_OFF_0X13_0X00,
            address=self._address,
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_CLEANUP, None),
            cmd2=self._group)
        template_fast_off_cleanup = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_OFF_FAST_0X14_0X00,
            address=self._address,
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_CLEANUP, None),
            cmd2=self._group)
        template_manual_on_cleanup = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_MANUALLY_TURNED_ON_0X23_0X00,
            address=self._address,
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_CLEANUP, None),
            cmd2=self._group)
        template_manual_off_cleanup = StandardReceive.template(
            commandtuple=COMMAND_LIGHT_MANUALLY_TURNED_OFF_0X22_0X00,
            address=self._address,
            flags=MessageFlags.template(MESSAGE_TYPE_ALL_LINK_CLEANUP, None),
            cmd2=self._group)

        self._message_callbacks.add(template_on_group,
                                    self._on_message_received)
        self._message_callbacks.add(template_fast_on_group,
                                    self._on_message_received)
        self._message_callbacks.add(template_off_group,
                                    self._off_message_received)
        self._message_callbacks.add(template_fast_off_group,
                                    self._off_message_received)
        self._message_callbacks.add(template_manual_on_group,
                                    self._manual_change_received)
        self._message_callbacks.add(template_manual_off_group,
                                    self._manual_change_received)

        self._message_callbacks.add(template_on_cleanup,
                                    self._on_message_received)
        self._message_callbacks.add(template_fast_on_cleanup,
                                    self._on_message_received)
        self._message_callbacks.add(template_off_cleanup,
                                    self._off_message_received)
        self._message_callbacks.add(template_fast_off_cleanup,
                                    self._off_message_received)
        self._message_callbacks.add(template_manual_on_cleanup,
                                    self._manual_change_received)
        self._message_callbacks.add(template_manual_off_cleanup,
                                    self._manual_change_received)


class OnOffSwitch(OnOffStateBase):
    """On/Off state representing an On/Off switch that is controllable.

    Available properties are:
      value
      name
      address
      group

    Available methods are:
      on()
      off()
      register_updates()
      async_refresh_state()
    """

    def on(self):
        """Send ON command to device."""
        on_command = StandardSend(self._address,
                                  COMMAND_LIGHT_ON_0X11_NONE, 0xff)
        self._send_method(on_command,
                          self._on_message_received)

    def off(self):
        """Send OFF command to device."""
        off_command = StandardSend(self._address,
                                   COMMAND_LIGHT_OFF_0X13_0X00)
        self._send_method(off_command,
                          self._off_message_received)


class OnOffSwitch_OutletTop(OnOffStateBase):
    """Device state representing a controllable top outlet On/Off switch.

    Available properties are:
      value
      name
      address
      group

    Available methods are:
      on()
      off()
      register_updates()
      async_refresh_state()
    """

    def __init__(self, address, statename, group, send_message_method,
                 message_callbacks, defaultvalue=None):
        """Initalize the OnOffSwitch_OutletTop Class."""
        super().__init__(address, statename, group, send_message_method,
                         message_callbacks, defaultvalue)

        self._updatemethod = self._send_status_0x01_request

    def on(self):
        """Send ON command to device."""
        on_command = StandardSend(self._address,
                                  COMMAND_LIGHT_ON_0X11_NONE, 0xff)
        self._send_method(on_command, self._on_message_received)

    def off(self):
        """Send OFF command to device."""
        self._send_method(StandardSend(self._address,
                                       COMMAND_LIGHT_OFF_0X13_0X00),
                          self._off_message_received)

    def _send_status_0x01_request(self):
        """Sent status request to device."""
        status_command = StandardSend(self._address,
                                      COMMAND_LIGHT_STATUS_REQUEST_0X19_0X01)
        self._send_method(status_command, self._status_message_0x01_received)

    def _status_message_0x01_received(self, msg):
        """Handle status received messages.

        The following status values can be recieve:
            0x00 = Both Outlets Off
            0x01 = Only Top Outlet On
            0x02 = Only Bottom Outlet On
            0x03 = Both Outlets On
        """
        if msg.cmd2 == 0x00 or msg.cmd2 == 0x02:
            self._update_subscribers(0x00)
        elif msg.cmd2 == 0x01 or msg.cmd2 == 0x03:
            self._update_subscribers(0xff)
        else:
            raise ValueError


class OnOffSwitch_OutletBottom(OnOffStateBase):
    """Device state representing a controllable bottom outlet On/Off switch.

    Available properties are:
      value
      name
      address
      group

    Available methods are:
      on()
      off()
      register_updates()
      async_refresh_state()
    """

    def __init__(self, address, statename, group, send_message_method,
                 set_message_callback_method, defaultvalue=None):
        """Initialize the OnOffSwitch_OutletBottom."""
        super().__init__(address, statename, group, send_message_method,
                         set_message_callback_method, defaultvalue)

        self._updatemethod = self._send_status_0x01_request
        self._udata = {'d1': self._group}

    def on(self):
        """Send an ON message to device group."""
        on_command = ExtendedSend(self._address,
                                  COMMAND_LIGHT_ON_0X11_NONE,
                                  self._udata,
                                  cmd2=0xff)
        on_command.set_checksum()
        self._send_method(on_command, self._on_message_received)

    def off(self):
        """Send an OFF message to device group."""
        off_command = ExtendedSend(self._address,
                                   COMMAND_LIGHT_OFF_0X13_0X00,
                                   self._udata)
        off_command.set_checksum()
        self._send_method(off_command, self._off_message_received)

    def _send_status_0x01_request(self):
        """Send a status request."""
        status_command = StandardSend(self._address,
                                      COMMAND_LIGHT_STATUS_REQUEST_0X19_0X01)
        self._send_method(status_command, self._status_message_received)

    def _status_message_received(self, msg):
        """A status message has been received.

        The following status values can be recieve:
            0x00 = Both Outlets Off
            0x01 = Only Top Outlet On
            0x02 = Only Bottom Outlet On
            0x03 = Both Outlets On
        """
        if msg.cmd2 == 0x00 or msg.cmd2 == 0x01:
            self._update_subscribers(0x00)
        elif msg.cmd2 == 0x02 or msg.cmd2 == 0x03:
            self._update_subscribers(0xff)
        else:
            raise ValueError


class OpenClosedRelay(OnOffStateBase):
    """Device state representing an Open/Close switch that is controllable.

    Available properties are:
      value
      name
      address
      group

    Available methods are:
      open()
      close()
      register_updates()
      async_refresh_state()
    """

    def open(self):
        """Send OPEN command to device."""
        open_command = StandardSend(self._address,
                                    COMMAND_LIGHT_ON_0X11_NONE, 0xff)
        self._send_method(open_command, self._open_message_received)

    def close(self):
        """Send CLOSE command to device."""
        close_command = StandardSend(self._address,
                                     COMMAND_LIGHT_OFF_0X13_0X00)
        self._send_method(close_command, self._close_message_received)

    def _open_message_received(self, msg):
        """An OPEN message has been received."""
        self._update_subscribers(0xff)

    def _close_message_received(self, msg):
        """A CLOSE message has been received."""
        self._update_subscribers(0x00)


class OnOffKeypadA(OnOffSwitch):
    """Device state for a controllable keypad button A On/Off switch."""

    def __init__(self, address, statename, group, send_message_method,
                 message_callbacks, defaultvalue, leds):
        super().__init__(address, statename, group, send_message_method,
                         message_callbacks, defaultvalue)

        self._updatemethod = self._send_status_request
        self._leds = leds

    def led_on(self):
        self._leds.on(self._group)

    def led_off(self):
        self._leds.off(self._group)

    def led_is_on(self):
        return self._leds.is_on(self._group)

    def _on_message_received(self, msg):
        super()._on_message_received(msg)
        self._leds.async_refresh_state()

    def _off_message_received(self, msg):
        super()._off_message_received(msg)
        self._leds.async_refresh_state()

    def _send_status_request(self):
        switch_status_msg = StandardSend(
            self._address, COMMAND_LIGHT_STATUS_REQUEST_0X19_0X00)
        self._send_method(switch_status_msg, self._status_message_received)


class OnOffKeypad(OnOffStateBase):
    """Device state representing a controllable keypad button On/Off switch."""

    def __init__(self, address, statename, group, send_message_method,
                 set_message_callback_method, defaultvalue=None,
                 loop=None, leds=None):
        """Initialize the OnOffKeypad Class."""
        super().__init__(address, statename, group, send_message_method,
                         set_message_callback_method, defaultvalue)

        self._leds = leds

        self._on_mask = 0
        self._off_mask = 0
        self._x10_house_code = 20   # 20 means none set
        self._x10_unit = 20         # 20 means none set
        self._ramp_rate = 0
        self._on_level = 0
        self._led_brightness = 0
        self._non_toggle_mask = 0
        self._led_bit_mask = 0
        self._x10_all_bit_mask = 0
        self._on_off_bit_mask = 0
        self._trigger_group_bit_mask = 0

        self._updatemethod = self._leds.async_refresh_state
        self._sent_property = {}
        self._loop = loop
        self._status_response_lock = asyncio.Lock(loop=self._loop)
        self._status_retries = 0
        self._status_received = False

    @property
    def on_mask(self):
        """Return button on mask."""
        return self._on_mask

    @property
    def off_mask(self):
        """Return button on mask."""
        return self._off_mask

    @property
    def x10_house_code(self):
        """Return button on mask."""
        return self._x10_house_code

    @property
    def x10_unit(self):
        """Return button on mask."""
        return self._x10_unit

    @property
    def ramp_rate(self):
        """Return button on mask."""
        return self._ramp_rate

    @property
    def led_brightness(self):
        """Return button on mask."""
        return self._led_brightness

    @property
    def non_toggle_mask(self):
        """Return button on mask."""
        return self._non_toggle_mask

    @property
    def x10_all_bit_mask(self):
        """Return button on mask."""
        return self._x10_all_bit_mask

    @property
    def on_off_bit_mask(self):
        """Return button on mask."""
        return self._on_off_bit_mask

    def on(self):
        """Turn on the LED for the button."""
        self._leds.on(self._group)

    def off(self):
        """Turn off the LED for the button."""
        self._leds.off(self._group)

    def led_is_on(self):
        """Return if the LED is on for the button."""
        return self._leds.is_on(self._group)

    def led_changed(self, addr, group, val):
        """Capture a change to the LED for this button."""
        self.log.debug("Button %d LED changed from %d to %d",
                       self._group, self._value, val)
        led_on = bool(val)
        if led_on != bool(self._value):
            self._update_subscribers(int(led_on))

    def set_on_mask(self, mask):
        """Set the on mask for the current group/button."""
        set_cmd = self._create_set_property_msg('_on_mask', 0x02, mask)
        self._send_method(set_cmd, self._property_set)

    def set_off_mask(self, mask):
        """Set the off mask for the current group/button."""
        set_cmd = self._create_set_property_msg('_off_mask', 0x03, mask)
        self._send_method(set_cmd, self._property_set)

    def set_x10_address(self, x10address):
        """Set the X10 address for the current group/button."""
        set_cmd = self._create_set_property_msg('_x10_house_code', 0x04,
                                                x10address)
        self._send_method(set_cmd, self._property_set)

    def set_ramp_rate(self, ramp_rate):
        """Set the X10 address for the current group/button."""
        set_cmd = self._create_set_property_msg('_ramp_rate', 0x05,
                                                ramp_rate)
        self._send_method(set_cmd, self._property_set)

    def set_on_level(self, val):
        """Set on level for the button/group."""
        set_cmd = self._create_set_property_msg("_on_level", 0x06,
                                                val)
        self._send_method(set_cmd, self._property_set)
        self._send_method(on_cmd, self._on_message_received)

    def set_led_brightness(self, brightness):
        """Set the LED brightness for the current group/button."""
        set_cmd = self._create_set_property_msg("_led_brightness", 0x07,
                                                brightness)
        self._send_method(set_cmd, self._property_set)

    def set_non_toggle_mask(self, non_toggle_mask):
        """Set the non_toggle_mask for the current group/button."""
        set_cmd = self._create_set_property_msg("_non_toggle_mask", 0x08,
                                                non_toggle_mask)
        self._send_method(set_cmd, self._property_set)

    def set_x10_all_bit_mask(self, x10_all_bit_mask):
        """Set the x10_all_bit_mask for the current group/button."""
        set_cmd = self._create_set_property_msg("_x10_all_bit_mask", 0x0a,
                                                x10_all_bit_mask)
        self._send_method(set_cmd, self._property_set)

    def set_trigger_group_bit_mask(self, trigger_group_bit_mask):
        """Set the trigger_group_bit_mask for the current group/button."""
        set_cmd = self._create_set_property_msg("_trigger_group_bit_mask",
                                                0x0c, trigger_group_bit_mask)
        self._send_method(set_cmd, self._property_set)

    def scene_on(self):
        """Trigger group/scene to ON level."""
        user_data = Userdata({'d1': self._group,
                              'd2': 0x00,
                              'd3': 0x00,
                              'd4': 0x11,
                              'd5': 0xff,
                              'd6': 0x00})
        self._set_sent_property(DIMMABLE_KEYPAD_SCENE_ON_LEVEL, 0xff)
        cmd = ExtendedSend(self._address,
                           COMMAND_EXTENDED_TRIGGER_ALL_LINK_0X30_0X00,
                           user_data)
        cmd.set_checksum()
        self.log.debug('Calling scene_on and sending reponse to '
                       '_received_scene_triggered')
        self._send_method(cmd, self._received_scene_triggered)

    def scene_off(self):
        """Trigger group/scene to OFF level."""
        user_data = Userdata({'d1': self._group,
                              'd2': 0x00,
                              'd3': 0x00,
                              'd4': 0x13,
                              'd5': 0x00,
                              'd6': 0x00})
        self._set_sent_property(DIMMABLE_KEYPAD_SCENE_ON_LEVEL, 0x00)
        cmd = ExtendedSend(self._address,
                           COMMAND_EXTENDED_TRIGGER_ALL_LINK_0X30_0X00,
                           user_data)
        cmd.set_checksum()
        self._send_method(cmd, self._received_scene_triggered)

    def scene_level(self, level):
        """Trigger group/scene to input level."""
        if level == 0:
            self.trigger_off()
        else:
            user_data = Userdata({'d1': self._group,
                                  'd2': 0x00,
                                  'd3': 0x00,
                                  'd4': 0x11,
                                  'd5': level,
                                  'd6': 0x00})
            self._set_sent_property(DIMMABLE_KEYPAD_SCENE_ON_LEVEL, level)
            cmd = ExtendedSend(self._address,
                               COMMAND_EXTENDED_TRIGGER_ALL_LINK_0X30_0X00,
                               user_data)
            cmd.set_checksum()
            self._send_method(cmd, self._received_scene_triggered)

    def extended_status_request(self):
        """Send status request for group/button."""
        self._status_received = False
        user_data = Userdata({'d1': self.group,
                              'd2': 0x00})
        cmd = ExtendedSend(self._address,
                           COMMAND_EXTENDED_GET_SET_0X2E_0X00,
                           userdata=user_data)
        cmd.set_checksum()
        self._send_method(cmd, self._status_message_received, True)

    def _on_message_received(self, msg):
        #if msg.cmd2 == 0x00:
        #    onlevel = 0xff
        #else:
        #    onlevel = msg.cmd2
        #self._update_subscribers(onlevel)
        if not self.led_is_on():
            self.log.debug("LED is off and button was turned on")
            self._update_subscribers(1)
            self._leds.manual_on(self._group)
        else:
            self.log.debug("LED is already on when button turned on?")

    def _off_message_received(self, msg):
        #self._update_subscribers(0x00)
        if self.led_is_on():
            self.log.debug("LED is on and button was turned off")
            self._update_subscribers(0)
            self._leds.manual_off(self._group)
        else:
            self.log.debug("LED is already off when button turned off?")

    def _manual_change_received(self, msg):
        self._updatemethod()

    def _status_message_received(self, msg):
        """Confirmation that the status message is coming.

        The real status message is the extended direct message.
        """
        self.log.debug('Status message was acknowledged')
        if self._loop:
            self.log.debug("Loop is defined")
        else:
            self.log.debug("Loop not defined")
        if not self._status_received:
            asyncio.ensure_future(self._confirm_status_received(),
                                  loop=self._loop)
        self.log.debug('Got here')

    @asyncio.coroutine
    def _confirm_status_received(self):
        self.log.debug("Confirming actual status is received")
        if self._status_received:
            self.log.debug('Status was received')
            return

        yield from self._status_response_lock
        try:
            with async_timeout.timeout(2):
                yield from self._status_response_lock
                self.log.debug("Actual status received")
        except asyncio.TimeoutError:
            self.log.debug('No status message received')
            if self._status_retries < 10:
                self.log.debug('Resending request')
                self._status_retries += 1
                self.extended_status_request()
            else:
                self.log.debug('Too many retries')
                self._status_retries = 0
        if self._status_response_lock.locked():
            self._status_response_lock.release()

    def _status_extended_message_received(self, msg):
        """ Status message received.:

            cmd1:  0x2e
            cmd2:  0x00
            flags: Direct Extended
            d1:    group
            d2:    0x01
            d3:    On Mask
            d4:    Off Mask
            d5:    X10 House Code
            d6:    X10 Unit
            d7:    Ramp Rate
            d8:    On-Level
            d9:    LED Brightness
            d10:   Non-Toggle Mask
            d11:   LED Bit Mask
            d12:   X10 ALL Bit Mask
            d13:   On/Off Bit Mask
            d14:   Check sum
        """
        self._status_received = True
        self._status_retries = 0
        self.log.debug("Extended status message received")
        if self._status_response_lock.locked():
            self._status_response_lock.release()
        user_data = msg.userdata
        #self._update_subscribers(user_data['d8'])
        self._set_status_data(user_data)

    def _property_set(self, msg):
        """Set command received and acknowledged."""
        prop = self._sent_property.get('prop')
        if prop and hasattr(self, prop):
            setattr(self, prop, self._sent_property.get('val'))
        self._sent_property = {}

    def _received_scene_triggered(self, msg):
        scene_level = self._sent_property.get('prop')
        val = self._sent_property.get('val')
        self.log.debug('Calling DimmableKeypad _received_scene_triggered '
                       'for group %s with on level %s',
                       self._group, scene_level)
        if scene_level == DIMMABLE_KEYPAD_SCENE_ON_LEVEL:
            #self._update_subscribers(val)
            self._leds.manual_on(self._group)

    def _set_status_data(self, userdata):
        """Set status properties from userdata response.

        Response values:
            d3:  On Mask
            d4:  Off Mask
            d5:  X10 House Code
            d6:  X10 Unit
            d7:  Ramp Rate
            d8:  On-Level
            d9:  LED Brightness
            d10: Non-Toggle Mask
            d11: LED Bit Mask
            d12: X10 ALL Bit Mask
            d13: On/Off Bit Mask
        """
        self._on_mask = userdata['d3']
        self._off_mask = userdata['d4']
        self._x10_house_code = userdata['d5']
        self._x10_unit = userdata['d6']
        self._ramp_rate = userdata['d7']
        self._on_level = userdata['d8']
        self._led_brightness = userdata['d9']
        self._non_toggle_mask = userdata['d10']
        self._led_bit_mask = userdata['d11']
        self._x10_all_bit_mask = userdata['d12']
        self._on_off_bit_mask = userdata['d13']
        self._trigger_group_bit_mask = userdata['d14']

    def _register_messages(self):
        super()._register_messages()
        template_status_recd = ExtendedReceive.template(
            address=self._address,
            commandtuple=COMMAND_EXTENDED_GET_SET_0X2E_0X00,
            # flags=MessageFlags.template(MESSAGE_TYPE_DIRECT_MESSAGE,
            #                             True),
            userdata={'d1': self._group,
                      'd2': 0x01})
        self._message_callbacks.add(template_status_recd,
                                    self._status_extended_message_received)

    def _create_set_property_msg(self, prop, cmd, val):
        """Create an extended message to set a property.

        Create an extended message with:
            cmd1: 0x2e
            cmd2: 0x00
            flags: Direct Extended
            d1: group
            d2: cmd
            d3: val
            d4 - d14: 0x00

        Parameters:
            prop: Property name to update
            cmd: Command value
                0x02: on mask
                0x03: off mask
                0x04: x10 house code
                0x05: ramp rate
                0x06: on level
                0x07: LED brightness
                0x08: Non-Toggle mask
                0x09: LED bit mask (Do not use in this class. Use LED class)
                0x0a: X10 All bit mask
                0x0c: Trigger group bit mask
            val: New property value
        """
        user_data = Userdata({'d1': self.group,
                              'd2': cmd,
                              'd3': val})
        msg = ExtendedSend(self._address,
                           COMMAND_EXTENDED_GET_SET_0X2E_0X00,
                           user_data)
        msg.set_checksum()
        self._set_sent_property(prop, val)
        return msg

    def _set_sent_property(self, prop, val):
        self._sent_property = {'prop': prop,
                               'val': val}


class OnOffKeypadLed(State):
    """Device state for KeyPadLinc LED."""

    def __init__(self, address, statename, group, send_message_method,
                 message_callbacks, defaultvalue=None, loop=None):
        super().__init__(address, statename, group, send_message_method,
                         message_callbacks, defaultvalue)

        self._updatemethod = self._send_status_request
        self._button_status_method = None

        self._loop = loop
        self._send_led_change_lock = asyncio.Lock(loop=self._loop)
        self._button_observer_callbacks = {}
        self._new_value = 0

    def on(self, group):
        """Turn the LED on for a group."""
        asyncio.ensure_future(self._send_led_on_off_request(group, 1),
                              loop=self._loop)

    def off(self, group):
        """Turn the LED off for a group."""
        asyncio.ensure_future(self._send_led_on_off_request(group, 0),
                              loop=self._loop)

    def manual_on(self, group):
        self._set_led_value(group, 1)
        self._send_status_request()

    def manual_off(self, group):
        self._set_led_value(group, 0)
        self._send_status_request()

    def is_on(self, group):
        """Returns if the LED for a button/group is on."""
        val = self._value & 1 << group - 1
        return bool(val)

    def register_led_updates(self, callback, button):
        """Register a callback when a specific button LED changes."""
        button_callbacks = self._button_observer_callbacks.get(button)
        if not button_callbacks:
            self._button_observer_callbacks[button] = []
        self.log.debug('New callback for button %d', button)
        self._button_observer_callbacks[button].append(callback)

    @asyncio.coroutine
    def _send_led_on_off_request(self, group, val):
        self.log.debug("OnOffKeypadLed._send_led_on_off_request was called")
        yield from self._send_led_change_lock
        self._new_value = set_bit(self._value, group, bool(val))

        user_data = Userdata({'d1': 0x01,
                              'd2': 0x09,
                              'd3': self._new_value})
        msg = ExtendedSend(self._address,
                           COMMAND_EXTENDED_GET_SET_0X2E_0X00,
                           user_data)
        msg.set_checksum()
        self._send_method(msg, self._on_off_ack_received, True)

    def _on_off_ack_received(self, msg):
        self._update_subscribers(self._new_value)
        if self._send_led_change_lock.locked():
            self._send_led_change_lock.release()

    def _send_status_request(self):
        led_status_msg = StandardSend(
            self._address, COMMAND_LIGHT_STATUS_REQUEST_0X19_0X01)
        self._send_method(led_status_msg, self._status_message_received)

    def _status_message_received(self, msg):
        self.log.debug("OnOffKeypadLed status message received with value 0x%02x", msg.cmd2)
        self.log.debug("Status message: %s", msg)
        self._update_subscribers(msg.cmd2)

    def _set_led_value(self, group, val):
        """Set the LED value and confirm with a status check."""
        new_bitmask = set_bit(self._value, group, bool(val))
        self._set_led_bitmask(new_bitmask)

    def _set_led_bitmask(self, bitmask):
        self._value = bitmask

    def _bit_value(self, group, val):
        """Set the LED on/off value from the LED bitmap."""
        bitshift = group - 1
        if val:
            new_value = self._value | (1 << bitshift)
        else:
            new_value = self._value & (0xff & ~(1 << bitshift))
        return new_value

    def _update_subscribers(self, val):
        old_value = self._value
        self._value = val
        for button in range(1, 9):
            old_bit_set = bit_is_set(old_value, button)
            new_bit_set = bit_is_set(self._value, button)
            old = 'on' if old_bit_set else 'off'
            new = 'on' if new_bit_set else 'off'
            self.log.debug('Button %d was %s now is %s', button, old, new)
            #if old_bit_set != new_bit_set:
            callbacks = self._button_observer_callbacks.get(button)
            if callbacks:
                for callback in callbacks:
                    self.log.debug('Calling button update callback %s', callback)
                    callback(self._address, button, int(new_bit_set))
            else:
                self.log.debug("No callbacks found for button %d", button)
