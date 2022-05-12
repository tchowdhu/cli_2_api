#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python example script showing proper use of the Cisco Sample Code header.
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


from __future__ import absolute_import, division, print_function


__author__ = "Tahsin Chowdhury <tchowdhu@cisco.com>"
__contributors__ = [
    "Tahsin Chowdhury <tchowdhu@cisco.com>"
]
__copyright__ = "Copyright (c) {{current_year}} Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


# Your code goes here.
indent = 4
print(
    __doc__,
    "Author:",
    " " * indent + __author__,
    "Contributors:",
    "\n".join([" " * indent + name for name in __contributors__]),
    "",
    __copyright__,
    "Licensed Under: " + __license__,
    sep="\n"
)

from pprint import pprint

import xmltodict as xmltodict
from ncclient import manager
from utils import *

# RPC filter for parsing interfaces stats
get_interface_stats_rpc="""
      <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
          <name>{intf_name}</name>
          <v4-protocol-stats>
            <in-pkts/>
            <in-error-pkts/>
          </v4-protocol-stats>
        </interface>
      </interfaces>
"""

#Setting threshold for max error
error_rate_threshold = 1e-9

#Connect to the device
devConnect = manager.connect(host=HOST,
                     port=PORT_NC,
                     username=USER,
                     password=PASSWD,
                     hostkey_verify=False,
                     look_for_keys = False)

#interface to check input errors and packet received
interface = "GigabitEthernet1"

input_packets = 0
input_errors = 0

#send payload to the device and print output
get_interface_stats_info = devConnect.get(filter=("subtree", get_interface_stats_rpc.format(intf_name=interface))).xml
get_interface_stats_dict = xmltodict.parse(get_interface_stats_info)["rpc-reply"]["data"]

print("\n ----------- Show RPC reply: ------------\n")
pprint(get_interface_stats_dict)

# Geting packets input and input errors from the RPC reply
input_packets = get_interface_stats_dict['interfaces'] ['interface'] ['v4-protocol-stats'] ['in-pkts']
input_errors = get_interface_stats_dict['interfaces'] ['interface'] ['v4-protocol-stats'] ['in-error-pkts']

print()
print("Show ratio of input errors and packet received:--------------------\n")
print('Interface {} Input Packets: {}'.format(interface, input_packets))
print('Interface {} Input Errors: {}'.format(interface, input_errors))

# Calculate packet loss ratio
packet_loss_ratio = float(input_errors)/float(input_packets)
result = 'FAIL'
if packet_loss_ratio < error_rate_threshold:
    result = 'PASS'
print('Interface {} Packet Loss Ratio:  {}:  {}'.format(interface, packet_loss_ratio, result))

devConnect.close_session()
