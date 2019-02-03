import pandas as pd
import datetime


def lldp_neighbour(device_name, output_str):
    """
    This function takes the raw output of 'show cdp neighbour' in cisco 2901 model routers
    and returns a pandas DataFrame of column 'local_device', 'local_port', 'remote_device', 'remote_port',
    'date', 'time'
    :param device_name: (type: str) name of the device from which the output was generated from
    :param output_str: (type: str) raw output generated from the command 'show cdp neighbour'
    :return: pandas DataFrame
    """
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()
    date = str(d.day) + '-' + str(d.month) + '-' + str(d.year)
    time = str(t.hour) + ':' + str(t.minute)

    connections = []
    top = 287
    bottom = -33
    trimmed_str = output_str[top:bottom]
    for line in trimmed_str.split('\n'):
        line_content = line.split()
        local_port = line_content[1] + line_content[2]
        remote_device = line_content[0].split('.')[0]
        remote_port = line_content[9] + line_content[10]
        connections.append([device_name.strip(), local_port.strip(), remote_device.strip(), remote_port.strip(),
                            date, time])

    connections_df = pd.DataFrame(connections, columns=['local_device', 'local_port', 'remote_device', 'remote_port',
                                                        'date', 'time'])
    return connections_df


def ram_usage(device_name, output_str):
    """
    This function takes the raw output of 'show processes memory | i Processor' in cisco 2901 model routers
    and returns a pandas DataFrame of column 'device_name', 'total_ram', 'currently_used', 'currently_free',
    'date', 'time'
    :param device_name: (type: str) name of the device from which the output was generated from
    :param output_str: (type: str) raw output generated from the command 'show processes memory | i Processor'
    :return: pandas DataFrame
    """
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()
    date = str(d.day) + '-' + str(d.month) + '-' + str(d.year)
    time = str(t.hour) + ':' + str(t.minute)

    output_contents = output_str.split(' ')
    total_ram = float(output_contents[4]) / 1000000  # converting Bytes to MegaBytes
    currently_used = float(output_contents[8]) / 1000000  # converting Bytes to MegaBytes
    currently_free = float(output_contents[11]) / 1000000  # converting Bytes to MegaBytes

    ram_df = pd.DataFrame([[device_name, total_ram, currently_used, currently_free, date, time]],
                          columns=['device_name', 'total_ram', 'currently_used', 'currently_free', 'date', 'time'])
    return ram_df


def cpu_usage(device_name, output_str):
    """
    This function takes the raw output of 'show processes cpu sorted | i CPU' in cisco 2901 model routers
    and returns a pandas DataFrame of column 'device_name', 'cpu_used', 'date', 'time'
    :param device_name: (type: str) name of the device from which the output was generated from
    :param output_str: (type: str) raw output generated from the command 'show processes cpu sorted | i CPU'
    :return: pandas DataFrame
    """
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()
    date = str(d.day) + '-' + str(d.month) + '-' + str(d.year)
    time = str(t.hour) + ':' + str(t.minute)

    output_contents = output_str.split(' ')
    cpu_used = output_contents[5].split('/')[0].strip('%')

    cpu_df = pd.DataFrame([[device_name, cpu_used, date, time]], columns=['device_name', 'cpu_used', 'date', 'time'])
    return cpu_df

