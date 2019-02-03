from database_helper.db_connection import db_connect
from networking_scripts.output_formatter import lldp_neighbour, ram_usage, cpu_usage
from networking_scripts.ssh import retrieve_cisco_data



# hostname = '192.168.10.100'
# lldp_output, ram_output, cpu_output = retrieve_cisco_data(hostname)

lldp_output ='''Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R1.fyp.com       Ser 0/0/0         132            R B S I CISCO2901 Ser 0/0/0
R1.fyp.com       Ser 0/0/1         132            R B S I CISCO2901 Ser 0/0/2

Total cdp entries displayed : 1'''


ram_output = '''Processor Pool Total:  289967796 Used:   36315344 Free:  253652452'''

cpu_output = '''CPU utilization for five seconds: 1%/0%; one minute: 0%; five minutes: 0%'''

int_stat_output = '''Interface                  IP-Address      OK? Method Status                Protocol
Embedded-Service-Engine0/0 unassigned      YES unset  administratively down down
GigabitEthernet0/0         192.168.10.100  YES manual up                    up
GigabitEthernet0/1         unassigned      YES unset  administratively down down
Serial0/0/0                10.0.0.1        YES manual up                    up
Serial0/0/1                unassigned      YES unset  administratively down down'''



hostname = 'R2'
connections_df = lldp_neighbour(hostname, lldp_output)
ram_df = ram_usage(hostname, ram_output)
cpu_df = cpu_usage(hostname, cpu_output)

connection, cursor = db_connect()

cursor.execute('''
insert into device_status
(
    device_name,
    total_ram,
    currently_used,
    currently_free,
    cpu_usage,
    collection_date,
    collection_time
)
values
(
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}'
)'''.format(ram_df['device_name'][0], ram_df['total_ram'][0], ram_df['currently_used'][0],
             ram_df['currently_free'][0], cpu_df['cpu_used'][0], cpu_df['date'][0], cpu_df['time'][0]))



for index, row in connections_df.iterrows():
    cursor.execute('''
    insert into connections
    (
        local_device,
        local_port,
        remote_device,
        remote_port,
        collection_date,
        collection_time
    )
    values
    (
        '{}',
        '{}',
        '{}',
        '{}',
        '{}',
        '{}'
    )'''.format(row['local_device'], row['local_port'], row['remote_device'], row['remote_port'],
                                                        row['date'], row['time']))


connection.commit()
connection.close()

