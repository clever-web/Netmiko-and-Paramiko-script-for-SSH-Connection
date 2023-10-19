from netmiko import SSHDetect, ConnectHandler
import paramiko

def establish_ssh_proxy(gateway_host, gateway_username, gateway_password, target_host, target_username, target_password):
    # Define the gateway (proxy) device details
    gateway_device = {
        'device_type': 'cisco_ios',  # Replace with the appropriate device type for your proxy
        'ip': gateway_host,
        'username': gateway_username,
        'password': gateway_password,
    }

    # Detect the SSH proxy's device type (you may need to adjust this)
    proxy_type = SSHDetect.find_device_type(**gateway_device)

    # Establish a connection to the SSH proxy
    with ConnectHandler(**gateway_device, device_type=proxy_type) as ssh_proxy:
        # Define the target (final) device details
        target_device = {
            'device_type': 'cisco_ios',  # Replace with the appropriate device type for your target devices
            'ip': target_host,
            'username': target_username,
            'password': target_password,
            'ssh_config_file': True,  # Use the system SSH configuration
            'proxy_command': f'ssh -W %h:%p -q {gateway_username}@{gateway_host}',  # ProxyCommand
        }

        # Establish a connection to the target device via the SSH proxy
        with ConnectHandler(**target_device) as net_connect:
            return net_connect.send_command("show version")

# Define your device and proxy details here
gateway_host = 'proxy_ip'
gateway_username = 'proxy_username'
gateway_password = 'proxy_password'
target_host = 'target_device_ip'
target_username = 'target_device_username'
target_password = 'target_device_password'

output = establish_ssh_proxy(gateway_host, gateway_username, gateway_password, target_host, target_username, target_password)
print(output)