import pandas as pd

from checks.process_alerts import insert_alerts_to_db
from config import all_devices, SEVERITY
from database_helper.query import execute_query
from database_helper.sql_statements import select_input_error, select_crc_error, select_frame_error, \
    select_overrun_error, select_ignored_error


def format_db_output(error_df, error_type, error_severity, output):
    """
    This functions takes a DataFrame which consists a specific type of "port error" data
    then it extracts the data and pass the formatted data to a database procedure
    :param error_df: a DataFrame of four columns
    :param error_type: input or crc or frame or overrun or ignored
    :param error_severity: alert or warning or danger
    :param output:
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

            output.append([device, code, error_severity, message, datetime])
    return output


def port_checker(device_list, severity=SEVERITY['port_error']):
    """
    ***IMPORTANT: this function requires to run right after "details_info_collector.py" scripts which collects all the port
    error of a given device***

    This function collects the most recent port errors from database
    then pass the data to another function to insert to a alert database from where the dashboard page will
    read its required data

    :param severity: warning
    :param device_list: list of all networking devices whose data is collected and stored in database
    :return: NONE
    """
    formatted_output = []
    for device_name in device_list:
        query = select_input_error(device_name)
        input_error_df = execute_query(query)
        formatted_output = format_db_output(input_error_df, 'input error', severity, formatted_output)

        query = select_crc_error(device_name)
        crc_error_df = execute_query(query)
        formatted_output = format_db_output(crc_error_df, 'crc error', severity, formatted_output)

        query = select_frame_error(device_name)
        frame_error_df = execute_query(query)
        formatted_output = format_db_output(frame_error_df, 'frame error', severity, formatted_output)

        query = select_overrun_error(device_name)
        overrun_error_df = execute_query(query)
        formatted_output = format_db_output(overrun_error_df, 'overrun error', severity, formatted_output)

        query = select_ignored_error(device_name)
        ignored_error_df = execute_query(query)
        formatted_output = format_db_output(ignored_error_df, 'ignored error', severity, formatted_output)

    error_df = pd.DataFrame(formatted_output, columns=['device_name', 'code', 'error_severity', 'message', 'date_time'])
    return error_df


def main():
    alerts_df = port_checker(all_devices, SEVERITY['port_error'])
    if not alerts_df.empty:
        insert_alerts_to_db(alerts_df)


if __name__ == '__main__':
    main()
