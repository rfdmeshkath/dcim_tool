import re
import datetime
import pandas as pd
from netmiko import ConnectHandler

from config import CISCO_LOGIN_INFO


def get_date_time():
    """
    This function gets current date and time and formats the information as per database requirement
    :return: string dd-mm-yyyy hh:mm
    """
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()
    date = str(d.day) + '-' + str(d.month) + '-' + str(d.year)
    time = str(t.hour) + ':' + str(t.minute)
    date_time = date + ' ' + time
    return date_time


class Cisco_3700:
    def __init__(self, device):
        self.device = device

    def get_total_ram(self):
        """
        This function connects to a device and retrieves ram usage
        :return: int (RAM usage in megabyte)
        """
        CISCO_LOGIN_INFO['device_type'] = 'cisco_ios'
        CISCO_LOGIN_INFO['ip'] = self.device
        # add try catch
        device = ConnectHandler(**CISCO_LOGIN_INFO)
        device.find_prompt()
        ram_str = device.send_command('show processes memory | include Processor')
        ram_df = self.ram_usage(ram_str)
        return round(ram_df['total_ram'].to_list()[0])

    def retrieve_data(self, device):
        """
        This function connects to a device and retrieves current "LLDP neighbor", CPU usage and RAM usage information
        :param device: device name of a device
        :return: pandas DataFrame
        """
        CISCO_LOGIN_INFO['device_type'] = 'cisco_ios'
        CISCO_LOGIN_INFO['ip'] = device
        # add try catch
        device = ConnectHandler(**CISCO_LOGIN_INFO)
        device.find_prompt()
        lldp_connections = device.send_command('show cdp neighbors')
        ram_usage = device.send_command('show processes memory | include Processor')
        cpu_usage = device.send_command('show processes cpu sorted | include CPU')
        errors = device.send_command('show interfaces | include CRC|Fast|Serial|Gig')
        unsed_port = device.send_command('show interfaces  | include line protocol is down')
        return lldp_connections, ram_usage, cpu_usage, errors, unsed_port

    def lldp_neighbour(self, output_str):
        """
        This function takes the raw output of a device which is a string and extract information from that
        string and makes a DataFrame
        :param output_str: string - LLDP neighbor output generated from a CISCO 3700 series device
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
        This function takes the raw RAM usage output from a networking device, then it extracts necessary data
         and then converts it to a DataFrame
        :param output_str: RAM usage output generated from a CISCO 3700 series device
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
        This function takes the raw CPU usage output from a networking device, then it extracts necessary data
         and then converts it to a DataFrame
        :param output_str: CPU usage output generated from a cisco 3700 series device
        :return: pandas DataFrame
        """

        date_time = get_date_time()
        output_contents = output_str.split(' ')
        cpu_used = output_contents[5].split('/')[0].strip('%')
        cpu_df = pd.DataFrame([[self.device, cpu_used, date_time]], columns=['device_name', 'cpu_used', 'date_time'])
        return cpu_df

    def get_errors(self, output_str):
        """
        This function extracts five types of errors (input,crc, overrun, frame, ignored) that might generate from a
        networking device.
        :param:port error output generated from a cisco 3700 series device
        :return: pandas DataFrame
        """
        date_time = get_date_time()
        trimmed_output = []
        all_errors = []
        line_counter = 0
        temp_lines = ''
        # trimming unnecessary lines from raw input
        for line in output_str.split('\n'):
            if 'protocol' in line or 'input errors' in line:
                line_counter = line_counter + 1
                temp_lines = temp_lines + line.strip() + ' '
                if line_counter == 2:
                    trimmed_output.append(temp_lines)
                    line_counter = 0
                    temp_lines = ''

        # extracting necessary information from each trimmed line
        for line in trimmed_output:
            # extracting port name
            port = re.search('(FastEthernet|Serial)\d*\W\d*', line).group(0)
            error_str = re.search('\d* input errors', line).group(0)
            input_error = re.search('\d*', error_str).group(0)
            # extracting crc error
            error_str = re.search('\d* CRC', line).group(0)
            crc_error = re.search('\d*', error_str).group(0)
            # extracting frame error
            error_str = re.search('\d* frame', line).group(0)
            frame_error = re.search('\d*', error_str).group(0)
            # extracting overrun error
            error_str = re.search('\d* overrun', line).group(0)
            overrun_error = re.search('\d*', error_str).group(0)
            # extracting ignored error
            error_str = re.search('\d* ignored', line).group(0)
            ignored_error = re.search('\d*', error_str).group(0)
            # appending to a temporary list which will be later converted to a DataFrame
            all_errors.append([self.device, port, input_error, crc_error, frame_error, overrun_error,
                               ignored_error, date_time])

        error_df = pd.DataFrame(all_errors, columns=['device_name', 'port', 'input', 'crc', 'frame', 'overrun',
                                                     'ignored', 'date_time'])
        return error_df

    def get_unused_ports(self, unused_port_str):
        """
        This function extracts all the unused ports of a device
        :param unused_port_str: raw output of unused ports from a cisco 3700 series device
        :return: pandas DataFrame
        """
        # if empty sting is passed then return empty DataFrame
        if unused_port_str == '':
            return pd.DataFrame()

        ports = []
        date_time = get_date_time()
        for line in unused_port_str.split('\n'):
            ports.append([self.device, line.strip().split(' ')[0], date_time])

        unused_port_df = pd.DataFrame(ports, columns=['device_name', 'port_name', 'date_time'])
        return unused_port_df

    def formatted_output(self):
        connections_str, ram_str, cpu_str, error_str, unused_port_str = self.retrieve_data(self.device)
        connection_df = self.lldp_neighbour(connections_str)
        ram_df = self.ram_usage(ram_str)
        cpu_df = self.cpu_usage(cpu_str)
        unused_port_df = self.get_unused_ports(unused_port_str)
        error_df = self.get_errors(error_str)

        return connection_df, ram_df, cpu_df, unused_port_df, error_df


# connection_df, ram_df, cpu_df, unused_port_df, error_df = Cisco_3700('R1').formatted_output()
# print(connection_df, ram_df, cpu_df, unused_port_df, error_df )