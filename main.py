import pandas as pd
from flask_cors import CORS
from flask import Flask, render_template, request, send_from_directory, session, jsonify, redirect

from apps.connections import insert_single_connection, get_connections
from apps.edit_connections import get_connection_details, change_manual_connection, delete_manual_connection
from apps.push_commands import get_user_inputs, execute_commands
from apps.resolve_alert import get_alert_info, resolve_alert_in_db
from apps.ticket_history import get_recent_tickets, get_searched_ticket
from apps.upload_connection import file_error_check, multiple_connection_insert
from authentication.ldap_auth import requires_auth
from apps.alerts_api import total_alerts_for_notification_icon, all_alerts_info
from apps.device_details import collect_data_for_device
from config import PRE_WRITTEN_COMMANDS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route('/api-total-alerts', methods=['GET'])
def get_total_alerts():
    alerts = total_alerts_for_notification_icon()
    return jsonify(alerts)


@app.route('/api-alerts-info', methods=['GET'])
def get_alerts_info():
    alerts_info = all_alerts_info()
    return jsonify(alerts_info)


@app.route('/', methods=['GET', 'POST'])
@requires_auth
def home():
    user = session.get('username')
    if request.method == 'GET':
        return render_template('home.html', user_name=user)


@app.route('/error', methods=['GET'])
def error():
    user = session.get('username')
    if request.method == 'GET':
        return render_template('error.html', user_name=user)


@app.route('/resolve-alert/<alert_id>', methods=['GET', 'POST'])
@requires_auth
def resolve_alert(alert_id):
    user = session.get('username')
    if request.method == 'GET':
        alert_info_dict = get_alert_info(alert_id)

        return render_template('resolve_alert.html', user_name=user,
                               dashboard_id=alert_info_dict['dashboard_id'], device_name=alert_info_dict['device_name'],
                               severity=alert_info_dict['severity'], alert_details=alert_info_dict['alert_details'],
                               occurred_datetime=alert_info_dict['occurred_datetime'],
                               resolved_hour=alert_info_dict['resolved_hour'],
                               resolved_minute=alert_info_dict['resolved_minute'])

    elif request.method == 'POST':
        resolve_status = resolve_alert_in_db(request.form, user)
        if resolve_status != 'success':
            return render_template('error.html', user_name=user)
        return redirect('/')


@app.route('/device-details', methods=['GET', 'POST'])
@requires_auth
def device_details():
    user = session.get('username')
    if request.method == 'GET':
        return render_template('device_details.html', user_name=user)

    elif request.method == 'POST':
        device_name = request.form.get('device_name')
        device_data = collect_data_for_device(device_name)
        return render_template('device_details.html', user_name=user, device_name=device_name,
                               system_name=device_data['system_name'], os_details=device_data['os_details'],
                               up_time=device_data['up_time'], total_ram=device_data['total_ram'],
                               cpu_x_axis=device_data['memory_timeline'], cpu_y_axis=device_data['cpu_usages'],
                               cpu_last_updated=device_data['memory_last_updated'],
                               ram_x_axis=device_data['memory_timeline'], ram_y_axis=device_data['ram_usages'],
                               ram_last_updated=device_data['memory_last_updated'],
                               lldp_table=device_data['lldp_connections_table'],
                               lldp_last_updated=device_data['lldp_last_updated'],
                               unused_ports=device_data['unused_ports'],
                               unused_ports_last_updated=device_data['unused_ports_last_updated'],
                               port_error_table=device_data['port_error_table'],
                               port_error_last_updated=device_data['port_error_last_updated'])


@app.route('/connections', methods=['GET', 'POST'])
@requires_auth
def search_connections():
    user = session.get('username')
    if request.method == 'GET':
        return render_template('connections.html', user_name=user)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Processing....':
        searched_item = request.form.get('searched_item')
        session['searched_item'] = searched_item
        connections_table = get_connections(searched_item)
        return render_template('connections.html', user_name=user, connections_table=connections_table)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Insert':
        insert_error = insert_single_connection(request.form)
        if insert_error == 'success':
            message = 'Connection insert was successful'
            return render_template('connections.html', user_name=user, success=message)
        else:
            return render_template('connections.html', user_name=user, error=insert_error)


@app.route('/connections/edit/<connection_id>', methods=['GET', 'POST'])
@requires_auth
def edit_connections(connection_id):
    user = session.get('username')
    if request.method == 'GET':
        connection_details_df = get_connection_details(connection_id)
        return render_template('edit_connection.html', user_name=user,
                               connection_id=connection_details_df['connection_id'][0],
                               local_device=connection_details_df['local_device'][0],
                               local_port=connection_details_df['local_port'][0],
                               remote_device=connection_details_df['remote_device'][0],
                               remote_port=connection_details_df['remote_port'][0],
                               interconnect_1=connection_details_df['interconnect_1'][0],
                               interconnect_2=connection_details_df['interconnect_2'][0])

    elif request.method == 'POST' and request.form['btn-identifier'] == 'Edit Connection':
        resolve_status = change_manual_connection(request.form, connection_id)
        searched_item = session.get('searched_item')
        connections_table = get_connections(searched_item)
        if resolve_status != 'success':
            return render_template('connections.html', user_name=user, connections_table=connections_table,
                                   error=resolve_status)
        return render_template('connections.html', user_name=user, connections_table=connections_table,
                               success='Connection Edited')

    elif request.method == 'POST' and request.form['btn-identifier'] == 'Delete':
        resolve_status = delete_manual_connection(connection_id)
        searched_item = session.get('searched_item')
        connections_table = get_connections(searched_item)
        if resolve_status != 'success':
            return render_template('connections.html', user_name=user, connections_table=connections_table,
                                   error=resolve_status)
        return render_template('connections.html', user_name=user, connections_table=connections_table,
                               success='Connection Deleted')


@app.route('/upload-connections', methods=['GET', 'POST'])
@requires_auth
def upload_connections():
    user = session.get('username')
    if request.method == 'GET':
        return render_template('upload_connections.html', user_name=user)

    # actions for button "Upload Excel File"
    elif request.method == 'POST' \
            and request.form['btn_identifier'] == 'Upload Excel File' \
            and request.files:
        connections_file = request.files['file']
        check_report, connections_df = file_error_check(connections_file)

        if check_report == 'success':
            connections_table = connections_df.to_html(classes=['table table-bordered'], header=True,
                                                       index=False, na_rep='')
            return render_template('upload_connections.html', user_name=user, connections_table=connections_table)
        else:
            return render_template('upload_connections.html', user_name=user, message=check_report)

    # actions for button "Download Template"
    elif request.method == 'POST' and request.form['btn_identifier'] == 'Download Template':
        return send_from_directory(directory='required_files', filename='Template.xlsx', as_attachment=True)

    # actions for button "Insert"
    elif request.method == 'POST' and request.form['btn_identifier'] == 'Insert':
        success_table, error_table = multiple_connection_insert()
        return render_template('upload_connections.html', user_name=user, error_message=error_table,
                               success_message=success_table)

    else:
        message = 'Choose the right Excel template'
        return render_template('upload_connections.html', user_name=user, message=message)


@app.route('/push-commands', methods=['GET', 'POST'])
@requires_auth
def send_commands():
    user = session.get('username')
    if request.method == 'GET':
        return render_template('push_commands.html', user_name=user, command_list=PRE_WRITTEN_COMMANDS.keys())
    else:
        device_name, port_name, command_option = get_user_inputs(request.form)
        status_s = execute_commands(device_name, port_name, command_option)
        return render_template('push_commands.html', user_name=user, command_list=PRE_WRITTEN_COMMANDS.keys(),
                               status=status_s)


@app.route('/ticket-history', methods=['GET', 'POST'])
@requires_auth
def search_history():
    user = session.get('username')
    if request.method == 'GET':
        recent_tickets_df = get_recent_tickets()
        recent_tickets_table = recent_tickets_df.to_html(classes=['table table-bordered'], header=True, index=False,
                                                         na_rep='')
        return render_template('ticket_history.html', user_name=user, tickets_table=recent_tickets_table)
    else:
        searched_item = request.form.get('searched_item')
        tickets_info_df = get_searched_ticket(searched_item)
        tickets_table = tickets_info_df.to_html(classes=['table table-bordered'], header=True, index=False, na_rep='')
        return render_template('ticket_history.html', user_name=user, tickets_table=tickets_table)


@app.route('/authentication-error', methods=['GET'])
def authentication_required():
    return render_template('authentication_required.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
