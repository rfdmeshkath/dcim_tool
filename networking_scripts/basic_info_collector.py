from config import SNMP_OID, all_devices
from database_helper.procedures import execute_procedure
from networking_scripts.device_scripts import Cisco_3700
from networking_scripts.snmp import collect_snmp_data


for device in all_devices:
    system_name = collect_snmp_data(device, SNMP_OID['sysName']).split('=')[1].strip()
    os_description = collect_snmp_data(device, SNMP_OID['sysDescr']).split('\n')[0].split('=')[1].strip()
    up_time = collect_snmp_data(device, SNMP_OID['sysUpTime']).split('=')[1].strip()
    # converting TimeTicks to hour
    up_time = round(int(up_time)/360000)
    total_ram = 0
    if 'Cisco' in os_description:
        total_ram = Cisco_3700(device).get_total_ram()

    # print('\n', system_name, '\n', os_description, '\n', up_time, '\n', total_ram)
    # update or insert these data to database
    status = execute_procedure('prc_insert_device_info', [device, system_name, os_description, up_time, total_ram])

    if status != 'success':
        print('logging system will be added here')
    else:
        print(status)