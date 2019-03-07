from apps.alerts_api import timestamp_to_string
from database_helper.query import execute_query
from database_helper.procedures import execute_procedure
from database_helper.sql_statements import select_alert_info


def get_alert_info(dashboard_id):
    query = select_alert_info(dashboard_id)
    alert_details_df = execute_query(query)
    alert_details_df.columns = ['dashboard_id', 'device_name', 'severity', 'alert_details', 'occurred_datetime']
    alert_details_df['occurred_datetime'] = timestamp_to_string(alert_details_df['occurred_datetime'][0])
    return alert_details_df


def resolve_alert_in_db(html_form_request, user_name):
    # retrieving user response from the "resolve_alert.html" form
    # alert_id, comment and resolved_datetime are the form input tag
    alert_id = html_form_request.get('alert_id')
    comment = html_form_request.get('comment')
    resolved_datetime = html_form_request.get('resolved_datetime')
    execution_status = execute_procedure('prc_resolve_alert', [alert_id, comment, resolved_datetime, user_name])
    return execution_status
