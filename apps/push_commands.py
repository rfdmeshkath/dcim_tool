from netmiko import ConnectHandler

from config import CISCO_PRIVILEGE_MODE_LOGIN_INFO, PRE_WRITTEN_COMMANDS


def get_user_inputs(html_from_request):
    """
    extract form information from POST request
    :param html_from_request: POST request object from HTML template
    :return: device_name, port_name, command_option chosen by user
    """
    device_name = html_from_request.get('device_name').lower()
    port_name = html_from_request.get('port_name')
    command_option = html_from_request.get('command_option')
    return device_name, port_name, command_option


def prepare_command(command_list, port_name):
    """
    replace "port_name with actual port name (e.g.:eth1, fa0/0)"
    :param command_list: list of prewritten command that need to be
            executed to perform desired task
    :param port_name: (optional) name of the port where modifications
            will be made
    :return: final executable command set
    """
    for i in range(0, len(command_list)):
        if 'port_name' in command_list[i]:
            command_list[i] = command_list[i].replace('port_name', port_name)
    return command_list


def ssh_client(device, commands):
    """
    This is a Secure shell cliend which can log into a networking
    device and execute commands
    :param device: name or IP address of device
    :param commands: list of executable commands
    :return: success or error status
    """
    try:
        # for now it is 'cisco_ios' is hard coded. but in functionality can be added to
        # check for device type and set "device_type" field dynamically
        # Netmiko supports cisco, arista, juniper, Linux, dell, huawei and many more device type
        CISCO_PRIVILEGE_MODE_LOGIN_INFO['device_type'] = 'cisco_ios'
        CISCO_PRIVILEGE_MODE_LOGIN_INFO['ip'] = device
        ssh_connection = ConnectHandler(**CISCO_PRIVILEGE_MODE_LOGIN_INFO)
        ssh_connection.enable()
        ssh_connection.config_mode()
        ssh_connection.send_config_set(commands)
        ssh_connection.disconnect()
        return 'success'
    except Exception as e:
        return 'error'


def execute_commands(device_s, port_name, command_option):
    """
    this function take all the user input then extract individual device name and port name
    and executes commands respectively
    :param device_s: DNS name of a single device or multiple device name separated by coma
    :param port_name: name of a port e.g.: eth1, fa0/1, gig0/2
    :param command_option: list of pre written commands
    :return: dictionary containing device name as key and success or error status as value
    """
    execution_status_response = {}
    # splitting multiple device names (if provided)
    device_s = device_s.split(',')
    if '' in device_s:
        device_s.remove('')
    commands = PRE_WRITTEN_COMMANDS[command_option]
    commands = prepare_command(commands, port_name)
    for device in device_s:
        status = ssh_client(device, commands)
        execution_status_response.update({device: status})
    return execution_status_response
