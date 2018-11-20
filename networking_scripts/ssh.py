from netmiko import ConnectHandler

login_info = {
  'device_type': 'cisco_ios',
  'ip': '192.168.11.2',
  'username': 'fyp',
  'password': 'cisco',
}

device = ConnectHandler(**login_info)
device.find_prompt()
output = device.send_command('show ip int brief')

print(output)
