from config import all_devices
from database_helper.procedures import execute_procedure
from database_helper.query import execute_query
from database_helper.sql_statements import select_input_error, select_crc_error, select_frame_error, \
    select_overrun_error, select_ignored_error


def insert_alerts_to_db(error_df, error_type):
    """
    This functions takes a DataFrame which consists a specific type of "port error" data
    then it extracts the data and pass the formatted data to a database procedure
    :param error_df: a DataFrame of four columns
    :param error_type: input or crc or frame or overrun or ignored
    :return: NONE
    """
    if not error_df.empty:
        error_df.columns = ['device_name', 'port_name', 'error_count', 'date_time']
        for index, row in error_df.iterrows():
            device = row['device_name']
            code = error_type.replace(' ', '_') + '_' + row['port_name']
            message = row['port_name'] + ' has ' + str(row['error_count']) + ' ' + error_type
            datetime = str(row['date_time'].date().day) + '-' + str(row['date_time'].date().month) + '-' + \
                       str(row['date_time'].date().year) + ' ' + str(row['date_time'].time().hour) + ':' + \
                       str(row['date_time'].time().minute)

            execution_status = execute_procedure('prc_insert_dashboard_alert', [device, code, message, datetime])
            if execution_status != 'success':
                print('failed ' + execution_status)


def check_for_alerts(all_devices):
    """
    ***IMPORTANT: this function requires to run right after "details_info_collector.py" scripts which collects all the port
    error of a given device***

    This function collects the most recent port errors from database
    then pass the data to another function to insert to a alert database from where the dashboard page will
    read its required data

    :param all_devices: list of all networking devices whose data is collected and stored in database
    :return: NONE
    """
    for device_name in all_devices:
        query = select_input_error(device_name)
        input_error_df = execute_query(query)
        insert_alerts_to_db(input_error_df, error_type='input error')

        query = select_crc_error(device_name)
        crc_error_df = execute_query(query)
        insert_alerts_to_db(crc_error_df, error_type='crc error')

        query = select_frame_error(device_name)
        frame_error_df = execute_query(query)
        insert_alerts_to_db(frame_error_df, error_type='frame error')

        query = select_overrun_error(device_name)
        overrun_error_df = execute_query(query)
        insert_alerts_to_db(overrun_error_df, error_type='overrun error')

        query = select_ignored_error(device_name)
        ignored_error_df = execute_query(query)
        insert_alerts_to_db(ignored_error_df, error_type='ignored error')


check_for_alerts(all_devices)
