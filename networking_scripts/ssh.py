from netmiko import ConnectHandler

from config import CISCO_LOGIN_INFO

device_address = '192.168.10.100'


def retrieve_cisco_data(device_address):
    CISCO_LOGIN_INFO['ip'] = device_address

    # int_stat = 'show ip interface brief'
    device = ConnectHandler(**CISCO_LOGIN_INFO)
    device.find_prompt()
    lldp_connections = device.send_command('show cdp neighbors')
    ram_usage = device.send_command('show processes memory | i Processor')
    cpu_usage = device.send_command('show processes cpu sorted | i CPU')

    return lldp_connections, ram_usage, cpu_usage
