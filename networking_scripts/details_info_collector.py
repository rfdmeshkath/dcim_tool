from config import all_devices, SNMP_OID
from database_helper.procedures import execute_procedure
from networking_scripts.device_scripts import Cisco_3700
from networking_scripts.snmp import collect_snmp_data

for device in all_devices:
    os_description = collect_snmp_data(device, SNMP_OID['sysDescr']).split('\n')[0].split('=')[1].strip()

    if 'Cisco' in os_description:
        connection_df, ram_df, cpu_df = Cisco_3700(device).formatted_output()

        # print('\n', connection_df, '\n', ram_df, '\n', cpu_df)
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
        else:
            print(con_status)

        mem_status = execute_procedure('prc_insert_memory_usage',
                                       [
                                        ram_df['device_name'][0],
                                        int(ram_df['currently_used'][0]),
                                        int(cpu_df['cpu_used'][0]),
                                        cpu_df['date_time'][0]
                                       ])

        if mem_status != 'success':
            print('failed ' + mem_status)
        else:
            print(mem_status)
