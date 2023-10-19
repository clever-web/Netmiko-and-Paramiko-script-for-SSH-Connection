#!/usr/bin/env python

import argparse
import getpass
import datetime
import sys
from netmiko import SSHDetect, ConnectHandler
from paramiko.proxy import SSHProxyCommand

print('\n============================================================')
print('Starting rlogin python script at :', datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S"))
print('============================================================\n')

# Define command line arguments
parser = argparse.ArgumentParser(description="Python Script to run commands on devices:")
parser.add_argument('-u', "--username", metavar='', help="Enter your username", default='cisco')
parser.add_argument('-p', "--password", metavar='', help="Enter your password")
parser.add_argument('-t', "--devicetype", metavar='', help="Specify the device type you are connecting to", default='cisco_nxos')
parser.add_argument("-c", "--commands", metavar='', help="Enter name file having commands to run", default='commands.txt')
parser.add_argument("-d", "--devices", metavar='', help="Enter name file having device names or IP addresses", default='devices.txt')
parser.add_argument("-op", "--prefix", metavar='', help="Enter Prefix for output file", default='')
parser.add_argument("-l", "--delay", metavar='', help="Enter delay factor", default=1)
# parser.add_argument("-l", "--ssh_proxy", metavar='', help="Enter delay factor", default='ssh -l user -i keyfile -o StrictHostKeyChecking=no -W %h:%p proxy_host')
parser.add_argument("--ssh_proxy", metavar='', help="Specify the SSH proxy command", default=None)
enable_grp = parser.add_mutually_exclusive_group()
enable_grp.add_argument("-e", "--enable", metavar='', help="Enter your enable password")
enable_grp.add_argument("-E", "--Enable", action="store_true", help="Pass enable password securely")
args = parser.parse_args()

# Global Variables
version = 'alpha0.1'

devices = []
commands = []
port = 22

if args.commands:
    with open(args.commands, 'r') as f:
        commands = f.read().splitlines()
else:
    command = input("Command:")
    commands.append(command)

if args.commands:
    device_file = args.devices
    with open(device_file, 'r') as f:
        devices = f.read().splitlines()
else:
    device = input("Device:")
    devices.append(device)

if not args.password:
    args.password = getpass.getpass(input("Remote Device Password:"))
    # args.password = getpass.getpass(prompt = "Remote Device Password:")

if args.Enable:
    args.enable = getpass.getpass()

now = datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S")

for device in devices:
    data = {
        'device_type': args.devicetype,
        'ip': device,
        'username': args.username,
        'password': args.password,
    }

    if args.enable:
        data['secret'] = args.enable

    # Add SSH Proxy configuration
    if args.ssh_proxy:
        proxy = SSHProxyCommand(args.ssh_proxy)
        data['ssh_config'] = {'proxy_command': proxy}

    # Establish an SSH connection to the device
    with ConnectHandler(**data) as net_connect:
        filename = ("./" + str(args.prefix) + '_' + str(device) + '_' + str(now) + ".txt")
        print("For device %s, sending output to the file %s\n" % (device, filename))

        for cmd in commands:
            output = net_connect.send_command(cmd)
            print(output)
            with open(filename, 'a+') as f:
                f.write(output)

print('============================================================')
print('Script successfully completed at :', datetime.datetime.now().strftime("%d-%b-%Y_%H-%M-%S"))
print('============================================================\n')

sys.exit()
