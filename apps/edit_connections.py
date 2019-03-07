from database_helper.procedures import execute_procedure
from database_helper.query import execute_query
from database_helper.sql_statements import select_connection_for_edit


def get_connection_details(connection_id):
    query = select_connection_for_edit(connection_id)
    connection_details_df = execute_query(query)
    connection_details_df.columns = ['connection_id', 'local_device', 'local_port', 'remote_device', 'remote_port',
                                     'interconnect_1', 'interconnect_2']
    return connection_details_df


def change_manual_connection(html_form_request, connection_id):
    # retrieving user response from the "resolve_alert.html" form
    # alert_id, comment and resolved_datetime are the form input tag
    local_device = html_form_request.get('local_device')
    local_port = html_form_request.get('local_port')
    remote_device = html_form_request.get('remote_device')
    remote_port = html_form_request.get('remote_port')
    interconnect_1 = html_form_request.get('interconnect_1')
    interconnect_2 = html_form_request.get('interconnect_2')
    execution_status = execute_procedure('prc_edit_manual_connection',
                                         [connection_id, local_device, local_port, remote_device, remote_port,
                                          interconnect_1, interconnect_2])
    return execution_status


def delete_manual_connection(connection_id):
    execution_status = execute_procedure('prc_delete_manual_connection', [connection_id])
    return execution_status
