import pandas as pd

from checks.process_alerts import insert_alerts_to_db
from config import all_devices, SEVERITY, UTILIZATION_THRESHOLD
from database_helper.query import execute_query
from database_helper.sql_statements import select_latest_memory_usage


def utilization_checker(device_list, ram_threshold, cpu_threshold, ram_severity, cpu_severity):
    alert_details = []
    for device in device_list:
        query = select_latest_memory_usage(device)
        utilization_df = execute_query(query)
        if not utilization_df.empty:
            utilization_df.columns = ['device_name', 'ram_usage', 'cpu_usage', 'date_time']
            for index, row in utilization_df.iterrows():
                if row['ram_usage'] > ram_threshold:
                    code = 'high_ram_util'
                    message = 'RAM utilization: ' + str(row['ram_usage'])
                    alert_founded = str(row['date_time'].date().day) + '-' + \
                                    str(row['date_time'].date().month) + '-' + \
                                    str(row['date_time'].date().year) + ' ' + \
                                    str(row['date_time'].time().hour) + ':' + \
                                    str(row['date_time'].time().minute)

                    alert_details.append([device, code, ram_severity, message, alert_founded])

                if row['cpu_usage'] > cpu_threshold:
                    code = 'high_cpu_util'
                    message = 'CPU utilization: ' + str(row['cpu_usage'])
                    alert_founded = str(row['date_time'].date().day) + '-' + \
                                    str(row['date_time'].date().month) + '-' + \
                                    str(row['date_time'].date().year) + ' ' + \
                                    str(row['date_time'].time().hour) + ':' + \
                                    str(row['date_time'].time().minute)

                    alert_details.append([device, code, cpu_severity, message, alert_founded])

    error_df = pd.DataFrame(alert_details, columns=['device_name', 'code', 'error_severity', 'message',
                                                    'date_time'])
    return error_df


def main():
    alerts_df = utilization_checker(all_devices, UTILIZATION_THRESHOLD['ram'], UTILIZATION_THRESHOLD['cpu'],
                                    SEVERITY['ram_utilization'], SEVERITY['cpu_utilization'])
    if not alerts_df.empty:
        insert_alerts_to_db(alerts_df)


if __name__ == '__main__':
    main()