import pandas as pd
import datetime

from netmiko import ConnectHandler

from config import CISCO_LOGIN_INFO


def get_date_time():
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()
    date = str(d.day) + '-' + str(d.month) + '-' + str(d.year)
    time = str(t.hour) + ':' + str(t.minute)
    date_time = date + ' ' + time
    return date_time


class Cisco_3700:
    def __init__(self, device):
        self.device = device

    def retrieve_data(self, device):
        CISCO_LOGIN_INFO['device_type'] = 'cisco_ios'
        CISCO_LOGIN_INFO['ip'] = device
        # add try catch
        device = ConnectHandler(**CISCO_LOGIN_INFO)
        device.find_prompt()
        lldp_connections = device.send_command('show cdp neighbors')
        ram_usage = device.send_command('show processes memory | i Processor')
        cpu_usage = device.send_command('show processes cpu sorted | i CPU')

        return lldp_connections, ram_usage, cpu_usage

    def lldp_neighbour(self, output_str):
        """
        This function takes the raw output of 'show cdp neighbour' in cisco routers
        and returns a pandas DataFrame of column 'local_device', 'local_port', 'remote_device', 'remote_port',
        'date', 'time'
        :param output_str: (type: str) raw output generated from the command 'show cdp neighbour'
        :return: pandas DataFrame
        """

        date_time = get_date_time()
        connections = []
        top = 212
        # bottom = -33
        trimmed_str = output_str[top:]
        for line in trimmed_str.split('\n'):
            line_content = line.split()
            local_port = line_content[1] + line_content[2]
            remote_device = line_content[0].split('.')[0]
            remote_port = line_content[8] + line_content[9]
            connections.append([self.device, local_port.strip(), remote_device.strip(), remote_port.strip(),
                                date_time])

        connections_df = pd.DataFrame(connections,
                                      columns=['local_device', 'local_port', 'remote_device', 'remote_port',
                                               'date_time'])
        return connections_df

    def ram_usage(self, output_str):
        """
        This function takes the raw output of 'show processes memory | i Processor' in cisco routers
        and returns a pandas DataFrame of column 'device_name', 'total_ram', 'currently_used', 'currently_free',
        'date', 'time'
        :param output_str: (type: str) raw output generated from the command 'show processes memory | i Processor'
        :return: pandas DataFrame
        """

        date_time = get_date_time()
        output_contents = output_str.split(' ')
        total_ram = float(output_contents[4]) / 1000000  # converting Bytes to MegaBytes
        currently_used = float(output_contents[8]) / 1000000  # converting Bytes to MegaBytes
        currently_free = float(output_contents[11]) / 1000000  # converting Bytes to MegaBytes

        ram_df = pd.DataFrame([[self.device, total_ram, currently_used, currently_free, date_time]],
                              columns=['device_name', 'total_ram', 'currently_used', 'currently_free', 'date_time'])
        return ram_df

    def cpu_usage(self, output_str):
        """
        This function takes the raw output of 'show processes cpu sorted | i CPU' in cisco routers
        and returns a pandas DataFrame of column 'device_name', 'cpu_used', 'date', 'time'
        :param output_str: (type: str) raw output generated from the command 'show processes cpu sorted | i CPU'
        :return: pandas DataFrame
        """

        date_time = get_date_time()
        output_contents = output_str.split(' ')
        cpu_used = output_contents[5].split('/')[0].strip('%')
        cpu_df = pd.DataFrame([[self.device, cpu_used, date_time]], columns=['device_name', 'cpu_used', 'date_time'])
        return cpu_df

    def get_total_ram(self):
        connections_str, ram_str, cpu_str = self.retrieve_data(self.device)
        ram_df = self.ram_usage(ram_str)
        return round(ram_df['total_ram'].to_list()[0])

    def formatted_output(self):
        connections_str, ram_str, cpu_str = self.retrieve_data(self.device)
        connection_df = self.lldp_neighbour(connections_str)
        ram_df = self.ram_usage(ram_str)
        cpu_df = self.cpu_usage(cpu_str)
        return connection_df, ram_df, cpu_df





