import datetime
import pandas as pd

from checks.process_alerts import insert_alerts_to_db
from config import all_devices, SEVERITY
from database_helper.query import execute_query
from database_helper.sql_statements import select_second_highest_date, select_disconnected_connections


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


def get_second_highest_datetime(device_name):
    query = select_second_highest_date(device_name)
    datetime_df = execute_query(query)
    datetime = datetime_df[0].dt.strftime('%d-%m-%Y %H:%M:%S').tolist()[0]
    return datetime


def disconnected_connection_checker(device_list, error_severity):
    alert_details = []
    for device in device_list:
        previous_datetime = get_second_highest_datetime(device)
        query = select_disconnected_connections(device, previous_datetime)
        disconnected_connections_df = execute_query(query)
        if not disconnected_connections_df.empty:
            disconnected_connections_df.columns = ['local_device', 'local_port', 'remote_device', 'remote_port']
            for index, row in disconnected_connections_df.iterrows():
                code = 'disconnected_connection_' + device + '_' + row['local_port']
                message = 'Connection Disconnected: ' + row['local_port'] + ' of ' + row['local_device'] + ' was ' + \
                          'connected to ' + row['remote_port'] + ' of ' + row['remote_device']
                alert_founded = get_date_time()
                alert_details.append([device, code, error_severity, message, alert_founded])
    error_df = pd.DataFrame(alert_details,  columns=['device_name', 'code', 'error_severity', 'message', 'date_time'])
    return error_df


def main():
    alerts_df = disconnected_connection_checker(all_devices, SEVERITY['disconnected_connection'])
    if not alerts_df.empty:
        insert_alerts_to_db(alerts_df)


if __name__ == '__main__':
    main()