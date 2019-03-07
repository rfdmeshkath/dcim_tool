import pandas as pd
from flask_cors import CORS
from flask import Flask, render_template, request, send_from_directory, session, jsonify, redirect

from apps.connections import insert_single_connection, get_connections
from apps.edit_connections import get_connection_details, change_manual_connection, delete_manual_connection
from apps.resolve_alert import get_alert_info, resolve_alert_in_db
from apps.upload_connection import file_error_check
from authentication.ldap_auth import requires_auth
from apps.alerts_api import total_alerts_for_notification_icon, all_alerts_info
from apps.device_details import collect_data_for_device

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
        alert_info_df = get_alert_info(alert_id)
        return render_template('resolve_alert.html', user_name=user,
                               alert_id=alert_info_df['dashboard_id'][0], device_name=alert_info_df['device_name'][0],
                               severity=alert_info_df['severity'][0], alert_details=alert_info_df['alert_details'][0],
                               occurred_datetime=alert_info_df['occurred_datetime'][0])
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
    elif request.method == 'POST' and request.form['btn_identifier'] == 'Upload Excel File' \
            and request.files:
        connections_file = request.files['file']
        file_error_check(connections_file)
        connections_df = pd.read_excel(connections_file)
        connections = connections_df.to_html(classes=['table table-bordered'], header=True, index=False)
        return render_template('upload_connections.html', user_name=user, connections_table=connections)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Download Template':
        return send_from_directory(directory='required_files', filename='Template.xlsx', as_attachment=True)

    else:
        return render_template('upload_connections.html', user_name=user)


@app.route('/authentication-error', methods=['GET'])
def authentication_required():
    return render_template('authentication_required.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run(debug=True)
