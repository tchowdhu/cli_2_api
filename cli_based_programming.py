#Optional libraries, for ignoring warnings
from cryptography import CryptographyDeprecationWarning
from warnings import filterwarnings, warn
filterwarnings("ignore")
warn("deprecated", CryptographyDeprecationWarning)

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

