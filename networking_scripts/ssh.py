from netmiko import ConnectHandler

from config import CISCO_LOGIN_INFO


def retrieve_cisco_data(device_address):
    CISCO_LOGIN_INFO['ip'] = device_address
    device = ConnectHandler(**CISCO_LOGIN_INFO)
    device.find_prompt()
    lldp_connections = device.send_command('show cdp neighbors')
    ram_usage = device.send_command('show processes memory | i Processor')
    cpu_usage = device.send_command('show processes cpu sorted | i CPU')

    return lldp_connections, ram_usage, cpu_usage
