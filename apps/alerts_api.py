from database_helper.query import execute_query
from database_helper.sql_statements import select_total_alerts, select_all_alerts_info


def timestamp_to_string(timestamp):
    time_str = 'Date: ' + str(timestamp.date().day) + '-' + str(timestamp.date().month) + '-' + \
               str(timestamp.date().year) + ' ' + \
               'Time: ' + str(timestamp.time().hour) + ':' + str(timestamp.time().minute)
    return time_str


def total_alerts_for_notification_icon():
    query = select_total_alerts()
    total_alerts_df = execute_query(query)
    if total_alerts_df.empty:
        alerts = ''
    else:
        alerts = int(total_alerts_df[0][0])
    return alerts


def all_alerts_info():
    query = select_all_alerts_info()
    alerts_info_df = execute_query(query)
    if not alerts_info_df.empty:
        alerts_info_df.columns = ['id', 'device_name', 'severity', 'error_details', 'date_time']
        alerts_info_df['date_time'] = alerts_info_df['date_time'].apply(timestamp_to_string)
        alerts_info_dict = alerts_info_df.to_dict('records')
        return alerts_info_dict
    return {}
