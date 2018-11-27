from __future__ import print_function
from pysnmp.entity.rfc3413.oneliner import cmdgen

COMMUNITY_STRING = 'fypreadsnmp'
SNMP_PORT = 161 # default snmp port
SNMP_HOST = '192.168.10.100'

sysDescr_OID = '.1.3.6.1.2.1.1.1.0'
sysUpTime_OID = '.1.3.6.1.2.1.1.3.0'
sysName = '.1.3.6.1.2.1.1.5.0'
cpu_util = '.1.3.6.1.4.1.14179.1.1.5.1' ##
display_errors = True

cmdGen = cmdgen.CommandGenerator()
snmp_target = (SNMP_HOST, SNMP_PORT)
cmd_gen = cmdgen.CommandGenerator()
(error_detected, error_status, error_index, snmp_data) = \
    cmd_gen.getCmd(cmdgen.CommunityData(COMMUNITY_STRING),
                   cmdgen.UdpTransportTarget(snmp_target), sysUpTime_OID,
                   lookupNames=True, lookupValues=True)
if not error_detected:
    print(snmp_data[0].prettyPrint())
else:
    if display_errors:
        print('ERROR DETECTED: ')
        print('    %-16s %-60s' % ('error_message', error_detected))
        print('    %-16s %-60s' % ('error_status', error_status))
        print('    %-16s %-60s' % ('error_index', error_index))
