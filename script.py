#This solution solves 90% of my problems
#!/usr/bin/env python

import argparse
from fileinput import close             # parse arguments
import socket               # TCP/Network/Socket
import getpass              # Get password in secure way
import datetime             # Date
import time
import sys                  # Used for Sys - Example sys.exit(), argumetns and others
from jumpssh import SSHSession # login to jumpbox ETC# Currently not used
from netmiko import ConnectHandler # SSH to clients


print ('\n============================================================')
print ('Starting rlogin python script at :', datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S"))
print ('============================================================\n')

parser = argparse.ArgumentParser(description="Python Script to run commands on devices:")

parser.add_argument('-u', "--username", metavar='', help="Enter your username", default='cisco')
parser.add_argument('-p', "--password", metavar='', help="Enter your password")
parser.add_argument('-t', "--devicetype", metavar='', help="Specify the device type you are connecting to", default='cisco_nxos')
parser.add_argument("-c", "--commands", metavar='', help="Enter name file having commands to run", default='commands.txt')
parser.add_argument("-d", "--devices", metavar='', help="Enter name file having devcie names or IP addresses", default='devices.txt')
parser.add_argument("-op", "--prefix", metavar='', help="Enter Prefix for output file", default='')
parser.add_argument("-l", "--delay", metavar='', help="Enter delay factor", default= 1)
enable_grp = parser.add_mutually_exclusive_group()
enable_grp.add_argument("-e", "--enable", metavar='', help="Enter your enable password")
enable_grp.add_argument("-E", "--Enable", action="store_true", help="Pass enable password securely")
args = parser.parse_args()

#Global Variables
version = 'alpha0.1'

devices = []
commands = []
timeout = 60
port = 22
#Set variables on basis of arguments received

input_data = {
    'Escape': "\n\n\n",
    '...\\r\\n^$': chr(3)
    }

"""
#challenges, why I want to use Netmiko

trying to send ctrl+c when I I see ... and a blank line after that, but not working, it infacts exit out of  the program
cisco_nexus# telnet 10.8.240.17 8980 vrf abc
Trying 10.8.240.17...


This is a success scnerio where I want to send three time enter to exit quickly
telnet: Unable to connect to remote host: Connection timed out
cisco_nexus# telnet 10.8.240.17 8080 vrf abc
Trying 10.8.240.17...
Connected to 10.8.240.17.
Escape character is '^]'.

"""
for pattern in input_data.keys():
    print(pattern)

if args.commands:
    with open(args.commands, 'r') as f:
     commands = f.read().splitlines()
else:
    command = raw_input("Command:")
    commands.append(command)

if args.commands:
    device_file = args.devices
    with open(device_file, 'r') as f:
      devices = f.read().splitlines()
else:
    device = raw_input("Device:")
    devices.append(device)

if not args.password:
    args.password = getpass.getpass(prompt = "Remote Device Password:")

if  args.Enable:
    args.enable = getpass.getpass()



jumpbox_pass = getpass.getpass(prompt = "Jumpbox Password:")
# establish ssh connection between your local machine and the jump server
gateway_session = SSHSession('basnycl001', username=args.username, password=jumpbox_pass).open()


for device in devices:
    data = {
    'device_type': args.devicetype,
    'host': device,
    'username': args.username,
    'password': args.password,
    }
    # from jump server, establish connection with a remote server
    remote_session = gateway_session.get_remote_session(data['host'], username=args.username, password=args.password)
    now = datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S")
    filename = ("./" + str(args.prefix) + '_' + str(device) + '_' + str(now) + ".txt")

    print ("For device  %s sending output to the file  %s \n" %(device, filename))
    

    for cmd in commands:
       # with ConnectHandler(**data) as net_connect:
        output =remote_session.get_cmd_output(cmd, timeout=5, input_data=input_data, continuous_output=True)
        print(output)
        with open(filename, 'a+') as f:
            f.write(output)
    remote_session.close()

print ('============================================================')
print ('Script successfully completed at :', datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S"))
print ('============================================================\n')

gateway_session.close()
sys.exit()



################Not working ########################################

#!/usr/bin/env python

import argparse
from fileinput import close             # parse arguments
import socket               # TCP/Network/Socket
import getpass              # Get password in secure way
import datetime             # Date
import time
import sys                  # Used for Sys - Example sys.exit(), argumetns and others
from jumpssh import SSHSession # login to jumpbox ETC# Currently not used
from netmiko import ConnectHandler # SSH to clients
import paramiko

print ('\n============================================================')
print ('Starting rlogin python script at :', datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S"))
print ('============================================================\n')

parser = argparse.ArgumentParser(description="Python Script to run commands on devices:")

parser.add_argument('-u', "--username", metavar='', help="Enter your username", default='abc')
parser.add_argument('-p', "--password", metavar='', help="Enter your password", default='abc')
parser.add_argument('-t', "--devicetype", metavar='', help="Specify the device type you are connecting to", default='cisco_nxos')
parser.add_argument("-c", "--commands", metavar='', help="Enter name file having commands to run", default='commands.txt')
parser.add_argument("-d", "--devices", metavar='', help="Enter name file having devcie names or IP addresses", default='devices.txt')
parser.add_argument("-op", "--prefix", metavar='', help="Enter Prefix for output file", default='')
parser.add_argument("-l", "--delay", metavar='', help="Enter delay factor", default= 1)
enable_grp = parser.add_mutually_exclusive_group()
enable_grp.add_argument("-e", "--enable", metavar='', help="Enter your enable password")
enable_grp.add_argument("-E", "--Enable", action="store_true", help="Pass enable password securely")
args = parser.parse_args()

#Global Variables
version = 'alpha0.1'

devices = []
commands = []
timeout = 60
port = 22
#Set variables on basis of arguments received

input_data = {
    'Escape': "\n\n\n",
    '...\\r\\n^$': chr(3) 
    }


for pattern in input_data.keys():
    print(pattern)

if args.commands:
    with open(args.commands, 'r') as f:
     commands = f.read().splitlines()
else:
    command = raw_input("Command:")
    commands.append(command)

if args.commands:
    device_file = args.devices
    with open(device_file, 'r') as f:
      devices = f.read().splitlines()
else:
    device = raw_input("Device:")
    devices.append(device)

if not args.password:
    args.password = getpass.getpass(prompt = "Remote Device Password:")

if  args.Enable:
    args.enable = getpass.getpass()



jumpbox_pass = getpass.getpass(prompt = "Jumpbox Password:")
# establish ssh connection between your local machine and the jump server
gateway_session = SSHSession('jumpbox', username=args.username, password=jumpbox_pass).open()


for device in devices:
    data = {
    'device_type': args.devicetype,
    'hostname': device,
    'username': args.username,
    'password': args.password,
    }
    # from jump server, establish connection with a remote server
    remote_session = gateway_session.get_remote_session(data['hostname'], username=args.username, password=args.password)
    now = datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S")
    filename = ("./" + str(args.prefix) + '_' + str(device) + '_' + str(now) + ".txt")


    print(remote_session)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(data['hostname'], 22, data['username'], data['password'], sock=remote_session)

    print(ssh)
    print ("For device  %s sending output to the file  %s \n" %(device, filename))
    

    for cmd in commands:
       # with ConnectHandler(**data) as net_connect:
        #output =remote_session.get_cmd_output(cmd, timeout=5, input_data=input_data, continuous_output=True)
        remote_session.send_command("show version" )
        print(output)
        with open(filename, 'a+') as f:
            f.write(output)
    remote_session.close()

print ('============================================================')
print ('Script successfully completed at :', datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S"))
print ('============================================================\n')

gateway_session.close()
sys.exit()


print output for debug
SSHSession(host=<snip>, username=<>snip, port=22, private_key_file=None, proxy_transport=<paramiko.Transport at 0xf49fa90 (cipher aes128-ctr, 128 bits) (active; 1 open channel(s))>)

Error
Traceback (most recent call last):
  File "C:\Users\snip\OneDrive - \Documents\Scripts\dashboard\test.py", line 94, in <module>
    ssh.connect(data['hostname'], 22, data['username'], data['password'], sock=remote_session)
  File "c:\Program Files\Python310\lib\site-packages\paramiko\client.py", line 413, in connect
    t = self._transport = transport_factory(
  File "c:\Program Files\Python310\lib\site-packages\paramiko\transport.py", line 457, in __init__
    self.sock.settimeout(self._active_check_timeout)
AttributeError: 'SSHSession' object has no attribute 'settimeout'. Did you mean: 'timeout'?
