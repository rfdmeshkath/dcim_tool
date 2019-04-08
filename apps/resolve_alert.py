import datetime

from apps.alerts_api import timestamp_to_string
from database_helper.query import execute_query
from database_helper.procedures import execute_procedure
from database_helper.sql_statements import select_alert_info


def get_alert_info(dashboard_id):
    alert_info_dict = {
        'dashboard_id': '',
        'device_name': '',
        'severity': '',
        'alert_details': '',
        'occurred_datetime': '',
        'resolved_hour': '',
        'resolved_minute': ''
    }

    query = select_alert_info(dashboard_id)
    alert_details_df = execute_query(query)
    alert_details_df.columns = ['dashboard_id', 'device_name', 'severity', 'alert_details', 'occurred_datetime']
    alert_info_dict['dashboard_id'] = alert_details_df['dashboard_id'][0]
    alert_info_dict['device_name'] = alert_details_df['device_name'][0]
    alert_info_dict['severity'] = alert_details_df['severity'][0]
    alert_info_dict['alert_details'] = alert_details_df['alert_details'][0]
    alert_info_dict['occurred_datetime'] = timestamp_to_string(alert_details_df['occurred_datetime'][0])
    alert_info_dict['resolved_hour'] = datetime.datetime.now().time().hour
    alert_info_dict['resolved_minute'] = datetime.datetime.now().time().minute
    return alert_info_dict


def resolve_alert_in_db(html_form_request, user_name):
    # retrieving user response from the "resolve_alert.html" form
    # alert_id, comment and resolved_datetime are the form input tag
    alert_id = html_form_request.get('dashboard_id')
    comment = html_form_request.get('comment')
    resolved_date = html_form_request.get('resolved_date')
    resolved_date = datetime.datetime.strptime(resolved_date, "%Y-%m-%d").strftime("%d-%m-%Y")
    resolved_hour = html_form_request.get('resolved_hour')
    resolved_minute = html_form_request.get('resolved_minute')
    resolved_datetime = resolved_date + ' ' + resolved_hour + ':' + resolved_minute  # datetime format
    execution_status = execute_procedure('prc_resolve_alert', [alert_id, comment, resolved_datetime, user_name])
    return execution_status
    # return 'success'