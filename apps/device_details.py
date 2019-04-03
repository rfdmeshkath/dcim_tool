from database_helper.query import execute_query
from database_helper.sql_statements import select_lldp_connections, select_memory_usage, select_device_info, \
    select_unused_ports, select_port_error


def collect_data_for_device(device_name):
    # setting default values to device_data
    # this function will return these default values if any device is not been found in database
    device_data = {
        'system_name': 'Device not Found',
        'os_details': 'n/a',
        'up_time': 'n/a',
        'total_ram': 'n/a',
        'memory_last_updated': 'n/a',
        'ram_usages': [],
        'cpu_usages': [],
        'memory_timeline': [],
        'lldp_last_updated': 'n/a',
        'lldp_connections_table': 'n/a',
        'unused_ports_last_updated': 'n/a',
        'unused_ports': 'n/a',
        'port_error_last_updated': 'n/a',
        'port_error_table': 'n/a'
    }

    query = select_device_info(device_name)
    device_info_df = execute_query(query)
    if not device_info_df.empty:
        device_info_df.columns = ['system_name', 'os_details', 'up_time', 'total_ram']
        device_data['system_name'] = device_info_df['system_name'][0]
        device_data['os_details'] = device_info_df['os_details'][0]
        device_data['up_time'] = device_info_df['up_time'][0]
        device_data['total_ram'] = device_info_df['total_ram'][0]

    query = select_memory_usage(device_name)
    memory_df = execute_query(query)
    if not memory_df.empty:
        memory_df = memory_df.iloc[::-1]
        memory_df.columns = ['device_name', 'ram_usage', 'cpu_usage', 'date_time']
        device_data['memory_last_updated'] = str(memory_df['date_time'][0])
        device_data['ram_usages'] = memory_df['ram_usage'].to_list()
        device_data['cpu_usages'] = memory_df['cpu_usage'].to_list()
        device_data['memory_timeline'] = memory_df['date_time'].dt.strftime('%H:%M').to_list()

    query = select_lldp_connections(device_name)
    lldp_connections_df = execute_query(query)
    if not lldp_connections_df.empty:
        lldp_connections_df.columns = ['Local Device', 'Local Port', 'Remote Device', 'Remote Port', 'date_time']
        device_data['lldp_last_updated'] = str(lldp_connections_df['date_time'][0])
        lldp_connections_df = lldp_connections_df.drop('date_time', 1) # 1 is for dropping column and 0 for dropping row
        device_data['lldp_connections_table'] = lldp_connections_df.to_html(classes=['table table-bordered'],
                                                                            table_id='dataTable', header=True,
                                                                            index=False)

    query = select_unused_ports(device_name)
    unused_ports_df = execute_query(query)
    if not unused_ports_df.empty:
        unused_ports_df.columns = ['device_name', 'port_name', 'date_time']
        device_data['unused_ports_last_updated'] = str(unused_ports_df['date_time'][0])
        port_names = unused_ports_df['port_name'].to_list()
        device_data['unused_ports'] = ' ,'.join(port_names)

    query = select_port_error(device_name)
    port_error_df = execute_query(query)
    if not port_error_df.empty:
        port_error_df.columns = ['Port Name', 'Input Error', 'CRC', 'Frame', 'Overrun', 'Ignored', 'date_time']
        device_data['port_error_last_updated'] = str(port_error_df['date_time'][0])
        port_error_df = port_error_df.drop('date_time', 1)  # 1 is for dropping column and 0 for dropping row
        device_data['port_error_table'] = port_error_df.to_html(classes=['table table-bordered'], header=True,
                                                                index=False)
    return device_data


