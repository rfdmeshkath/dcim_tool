import pandas as pd

from config import SNMP_OID
from networking_scripts.device_scripts import Cisco_2900, Cisco_3700
from networking_scripts.snmp import collect_snmp_data


def info_collector_test(device):
    connection_df = pd.DataFrame()
    ram_df = pd.DataFrame()
    cpu_df = pd.DataFrame()
    unused_port_df = pd.DataFrame()
    error_df = pd.DataFrame()

    system_name = collect_snmp_data(device, SNMP_OID['sysName']).split('=')[1].strip()
    os_description = collect_snmp_data(device, SNMP_OID['sysDescr']).split('\n')[0].split('=')[1].strip()
    up_time = collect_snmp_data(device, SNMP_OID['sysUpTime']).split('=')[1].strip()

    if 'Cisco' in os_description and 'C2900' in os_description:
        connection_df, ram_df, cpu_df, unused_port_df, error_df = Cisco_2900(device).formatted_output()
    elif 'Cisco' in os_description and '3700' in os_description:
        connection_df, ram_df, cpu_df, unused_port_df, error_df = Cisco_3700(device).formatted_output()

    return system_name, os_description, up_time, connection_df, ram_df, cpu_df, unused_port_df, error_df


if __name__ == '__main__':
    system_name, os_description, up_time, connection_df, ram_df, cpu_df, unused_port_df, error_df = \
        info_collector_test('R1')
    print(system_name, os_description, up_time, connection_df, ram_df, cpu_df, unused_port_df, error_df)
