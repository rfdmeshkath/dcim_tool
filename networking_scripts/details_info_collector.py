import pandas as pd

from config import all_devices, SNMP_OID
from database_helper.procedures import execute_procedure
from networking_scripts.device_scripts import Cisco_3700, Cisco_2900
from networking_scripts.snmp import collect_snmp_data

for device in all_devices:
    os_description = collect_snmp_data(device, SNMP_OID['sysDescr'])
    if os_description == '':
        print('could not establish connection')
        break

    connection_df = pd.DataFrame()
    ram_df = pd.DataFrame()
    cpu_df = pd.DataFrame()
    unused_port_df = pd.DataFrame()
    error_df = pd.DataFrame()

    if 'Cisco' in os_description and 'C2900' in os_description:
        connection_df, ram_df, cpu_df, unused_port_df, error_df = Cisco_2900(device).formatted_output()
    elif 'Cisco' in os_description and '3700' in os_description:
        connection_df, ram_df, cpu_df, unused_port_df, error_df = Cisco_3700(device).formatted_output()

    # update or insert these data to database
    if not connection_df.empty:
        for index, row in connection_df.iterrows():
            insert_status = execute_procedure('prc_insert_lldp_connection',
                                              [
                                                  row['local_device'],
                                                  row['local_port'],
                                                  row['remote_device'],
                                                  row['remote_port'],
                                                  row['date_time']
                                              ])
            if insert_status != 'success':
                print('failed ' + insert_status)

    if not ram_df.empty:
        mem_status = execute_procedure('prc_insert_memory_usage',
                                       [
                                           ram_df['device_name'][0],
                                           int(ram_df['currently_used'][0]),
                                           int(cpu_df['cpu_used'][0]),
                                           cpu_df['date_time'][0]
                                       ])

        if mem_status != 'success':
            print('failed ' + mem_status)

    if not unused_port_df.empty:
        for index, row in unused_port_df.iterrows():
            unused_port_status = execute_procedure('prc_insert_unused_port',
                                                   [
                                                       row['device_name'],
                                                       row['port_name'],
                                                       row['date_time']
                                                   ])

            if unused_port_status != 'success':
                print('failed ' + unused_port_status)

    if not error_df.empty:
        for index, row in error_df.iterrows():
            port_error_status = execute_procedure('prc_insert_port_error',
                                                  [
                                                      row['device_name'],
                                                      row['port'],
                                                      int(row['input']),
                                                      int(row['crc']),
                                                      int(row['frame']),
                                                      int(row['overrun']),
                                                      int(row['ignored']),
                                                      row['date_time'],
                                                  ])

            if port_error_status != 'success':
                print('failed ' + port_error_status)

    else:
        print('data extractor class is not present for {}'.format(device))
