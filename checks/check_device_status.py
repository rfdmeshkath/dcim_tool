import datetime
import pandas as pd

from checks.process_alerts import insert_alerts_to_db
from config import all_devices, SEVERITY
from networking_scripts.ping import check_if_device_is_reachable


def get_date_time():
    """
    This function gets current date and time and formats the information as per database requirement
    :return: string dd-mm-yyyy hh:mm
    """
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()
    date = str(d.day) + '-' + str(d.month) + '-' + str(d.year)
    time = str(t.hour) + ':' + str(t.minute)
    date_time = date + ' ' + time
    return date_time


def downstate_checker(devices_list, error_severity=SEVERITY['host_unreachable']):
    """
    This function checks if the device is up or not
    :param devices_list:
    :param error_severity:
    :return:
    """
    not_reachable = check_if_device_is_reachable(devices_list)
    unreachable_hosts_df = pd.DataFrame(columns=['device_name', 'code', 'error_severity', 'message', 'date_time'])
    if len(not_reachable) > 0:
        date_time = get_date_time()
        counter = 0
        for device in not_reachable:
            code = 'unreachable_' + device
            message = 'Device not reachable'
            unreachable_hosts_df.loc[counter] = [device, code, error_severity, message, date_time]
            counter = counter + 1
        return unreachable_hosts_df
    else:
        return pd.DataFrame()


def main():
    alerts_df = downstate_checker(all_devices, SEVERITY['host_unreachable'])
    if not alerts_df.empty:
        insert_alerts_to_db(alerts_df)


if __name__ == '__main__':
    main()
