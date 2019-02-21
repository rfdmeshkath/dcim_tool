from config import all_devices, SNMP_OID
from database_helper.procedures import execute_procedure
from networking_scripts.device_scripts import Cisco_3700
from networking_scripts.snmp import collect_snmp_data

for device in all_devices:
    os_description = collect_snmp_data(device, SNMP_OID['sysDescr'])

    if 'Cisco' in os_description:
        connection_df, ram_df, cpu_df, unused_port_df, error_df = Cisco_3700(device).formatted_output()

        # update or insert these data to database
        con_status = execute_procedure('prc_insert_lldp_connection',
                                       [
                                           connection_df['local_device'][0],
                                           connection_df['local_port'][0],
                                           connection_df['remote_device'][0],
                                           connection_df['remote_port'][0],
                                           connection_df['date_time'][0]
                                       ])
        if con_status != 'success':
            print('failed ' + con_status)

        mem_status = execute_procedure('prc_insert_memory_usage',
                                       [
                                           ram_df['device_name'][0],
                                           int(ram_df['currently_used'][0]),
                                           int(cpu_df['cpu_used'][0]),
                                           cpu_df['date_time'][0]
                                       ])

        if mem_status != 'success':
            print('failed ' + mem_status)

        unused_port_status = execute_procedure('prc_insert_unused_port',
                                               [
                                                   unused_port_df['device_name'][0],
                                                   unused_port_df['port_name'][0],
                                                   unused_port_df['date_time'][0]
                                               ])

        if unused_port_status != 'success':
            print('failed ' + unused_port_status)

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
