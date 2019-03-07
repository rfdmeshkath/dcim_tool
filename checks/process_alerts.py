from alerts.message import send_message
from alerts.email import send_email
from config import MONITOR_PHONE, MONITOR_EMAIL
from database_helper.procedures import execute_procedure
from database_helper.query import execute_query
from database_helper.sql_statements import select_notification_status


def insert_alerts_to_db(error_df):
    for index, row in error_df.iterrows():
        execution_status = execute_procedure('prc_insert_dashboard_alert', [row['device_name'],
                                                                            row['code'],
                                                                            row['error_severity'],
                                                                            row['message'],
                                                                            row['date_time']])
        if execution_status != 'success':
            print('prc_insert_dashboard_alert failed ' + execution_status)

        query = select_notification_status(row['device_name'], row['code'])
        notification_df = execute_query(query)
        notification_df.columns = ['notification_id', 'text_message', 'email']
        notification_id = int(notification_df['notification_id'][0])

        if row['error_severity'] == 'danger':
            if notification_df['text_message'][0] == 0:
                for each_number in MONITOR_PHONE:
                    message_body = 'Notification from Network Manager : \nDevice- ' + row['device_name'] + \
                                   '\nDetails: ' + row['message']
                    send_message(each_number, message_body)
                    execution_status = execute_procedure('prc_update_message_status', [notification_id])
                    if execution_status != 'success':
                        print('prc_update_message_status failed ' + execution_status)

        if row['error_severity'] == 'danger' or row['error_severity'] == 'warning':
            if notification_df['email'][0] == 0:
                for each_email in MONITOR_EMAIL:
                    email_subject = 'Notification from Network Manager regarding ' + row['device_name']
                    email_body = 'Device- ' + row['device_name'] + '\nDetails: ' + row['message']
                    send_email(each_email, email_subject, email_body)
                    execution_status = execute_procedure('prc_update_email_status', [notification_id])
                if execution_status != 'success':
                    print('prc_update_email_status failed ' + execution_status)
