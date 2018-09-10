#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# scalar_client                                                                #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# The program is a scalar client.                                              #
#                                                                              #
# copyright (C) 2018 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

import datetime
import time
import sys

import pyprel
import scalar

name        = "SCALAR CLIENT"
__version__ = "2018-09-10T2016Z"

def main():
    scalar.setup()
    scalar.room.backfill_previous_messages(limit = 20)
    scalar.room.add_listener(on_message)
    scalar.client.start_listener_thread()
    display_refresh()
    while True:
        message = get_input()
        if message.lower() in ["exit", "quit"]:
            terminal_flash_clear()
            line()
            print(pyprel.center_string("EXIT"))
            line()
            time.sleep(0.5)
            line()
            terminal_flash_clear()
            sys.exit(0)
        else:
            scalar.room.send_text(message)
            time.sleep(0.1)

def display_refresh():
    members         = [user.get_display_name() for user in scalar.room.get_joined_members()]
    events          = scalar.room.get_events()[10:]
    datetimes       = [datetime.datetime.fromtimestamp(event["origin_server_ts"] / 1000) for event in events]
    senders         = [event["sender"] for event in events]
    senders         = [sender.split("@")[1].split(":")[0] for sender in senders]
    messages        = [event["content"]["body"] for event in events]
    table_contents  = [["MEMBERS", "DATETIMES", "SENDERS", "MESSAGES"]]
    height_contents = int(0.5 * pyprel.terminal_height() - 0.5) - 3
    members         = members + ["" for blank in list(range(1, height_contents - len(members)))]
    datetimes       =           ["" for blank in list(range(1, height_contents - len(datetimes)))] + datetimes
    senders         =           ["" for blank in list(range(1, height_contents - len(senders)))]   + senders
    messages        =           ["" for blank in list(range(1, height_contents - len(messages)))]  + messages
    for member, _datetime, sender, message in zip(members, datetimes, senders, messages):
        table_contents.append([member, _datetime, sender, message])
    terminal_flash_clear()
    logo()
    print(pyprel.Table(
        contents              = table_contents,
        column_delimiter      = " ",
        row_delimiter         = " ",
        table_width_requested = None #50
    ))

def line():
    pyprel.print_line(character = "─")

def logo():
    line()
    print(pyprel.center_string(text = name + "       VERSION " + __version__))
    line()

def terminal_white():
    print(chr(27) + "[?5h")

def terminal_black():
    print(chr(27) + "[?5l")

def terminal_clear():
    print(chr(27) + "[2J")

def terminal_flash_clear():
    terminal_white()
    time.sleep(0.05)
    terminal_black()
    terminal_clear()

def get_input(prompt ="> "):
    if sys.version_info >= (3, 0):
        return input(prompt)
    else:
        return raw_input(prompt)

def on_message(room, event):
    if event["type"] == "m.room.message": display_refresh()

if __name__ == "__main__":
    main()
