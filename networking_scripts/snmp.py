from __future__ import print_function
from pysnmp.entity.rfc3413.oneliner import cmdgen

from config import SNMP_DETAILS, SNMP_OID


def collect_snmp_data(hostname, oid):
    cmdGen = cmdgen.CommandGenerator()
    snmp_target = (hostname, SNMP_DETAILS['port'])
    cmd_gen = cmdgen.CommandGenerator()
    (error_detected, error_status, error_index, snmp_data) = \
        cmd_gen.getCmd(cmdgen.CommunityData(SNMP_DETAILS['community_string']), cmdgen.UdpTransportTarget(snmp_target),
                       oid, lookupNames=True, lookupValues=True)
    if not error_detected:
        print(snmp_data[0].prettyPrint())
    else:
        print('ERROR DETECTED: ')
        print('    %-16s %-60s' % ('error_message', error_detected))
        print('    %-16s %-60s' % ('error_status', error_status))
        print('    %-16s %-60s' % ('error_index', error_index))


collect_snmp_data('192.168.10.100', SNMP_OID['sysUpTime'])
