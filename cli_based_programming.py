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


#import library to connect to the networking device
from netmiko import ConnectHandler
from utils import *

# Device information
device = {
    'ip': HOST,
    'username': USER,
    'password': PASSWD,
    'device_type': DEVICE_TYPE,
    'port': SSH_PORT
}

#Setting threshold for max error
error_rate_threshold = 1e-9

#Connect to the device
devConnect = ConnectHandler(**device)

#interface to check input errors and packet received
interface = "GigabitEthernet1"

#show command to get required statistics
show_command = 'show interface {}'.format(interface)
#input_packets = 0
#input_errors = 0

#send command to the device and print output
output = devConnect.send_command(show_command)
print("\n ----------- Show command output: ------------\n")
print(output)

#Breaking the output into separate lines
output = output.strip().split('\n')

# Search for each line for packets input and extract the info
#input_packets = int([item for (index, item) in enumerate(output) if 'packets input' in item][0].strip().split('packets input')[0].strip())
for item in output:
    if 'packets input' in item:
        print("\n ----------- Finding the info contaning packets input: ------------\n")
        #print(item)
        input_packets = int(item.strip().split('packets input')[0].strip())
        break

print()
print('Interface {} Input Packets: {}'.format(interface, input_packets))

# Search for each line for input errors and extract the info
#input_errors = int([item for (index, item) in enumerate(output) if 'input errors' in item][0].strip().split('input errors')[0].strip())

for item in output:
    if 'input errors' in item:
        print("\n ----------- Finding the info contaning input errors: ------------\n")
        #print(item)
        input_errors = int(item.strip().split('input errors')[0].strip())
        break

print()
print('Interface {} Input Errors: {}'.format(interface, input_errors))

# Calculate packet loss ratio
packet_loss_ratio = float(input_errors)/float(input_packets)
result = 'FAIL'
if packet_loss_ratio < error_rate_threshold:
    result = 'PASS'
print('Interface {} Packet Loss Ratio:  {}:  {}'.format(interface, packet_loss_ratio, result))

devConnect.disconnect()

