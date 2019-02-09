from database_helper.query import execute_query
from database_helper.sql_statements import select_lldp_connections, select_memory_usage, select_device_info


def collect_data_for_device(device_name):
    device_data = {}
    query = select_device_info(device_name)
    device_info_df = execute_query(query)
    device_info_df.columns = ['system_name', 'os_details', 'up_time', 'total_ram']
    device_data['system_name'] = device_info_df['system_name'][0]
    device_data['os_details'] = device_info_df['os_details'][0]
    device_data['up_time'] = device_info_df['up_time'][0]
    device_data['total_ram'] = device_info_df['total_ram'][0]

    query = select_memory_usage(device_name)
    memory_df = execute_query(query)
    memory_df = memory_df.iloc[::-1]
    memory_df.columns = ['device_name', 'ram_usage', 'cpu_usage', 'date_time']
    device_data['memory_last_updated'] = str(memory_df['date_time'][0])
    device_data['ram_usages'] = memory_df['ram_usage'].to_list()
    device_data['cpu_usages'] = memory_df['cpu_usage'].to_list()
    device_data['memory_timeline'] = memory_df['date_time'].dt.strftime('%H:%M').to_list()

    query = select_lldp_connections(device_name)
    lldp_connections_df = execute_query(query)
    lldp_connections_df.columns = ['Local Device', 'Local Port', 'Remote Device', 'Remote Port', 'date_time']
    device_data['lldp_last_updated'] = str(lldp_connections_df['date_time'][0])
    lldp_connections_df = lldp_connections_df.drop('date_time', 1)
    device_data['lldp_connections_table'] = lldp_connections_df.to_html(classes=['table table-bordered'],
                                                                     table_id='dataTable',
                                                                     header=True, index=False)
    return device_data


# a = collect_data_for_device('R1')
# print(a)
