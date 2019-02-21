import pandas as pd
from flask import Flask, render_template, request, send_from_directory, session

from apps.device_details import collect_data_for_device
from authentication.ldap_auth import requires_auth

app = Flask(__name__)
app.secret_key = 'key'


@app.route('/', methods=['GET', 'POST'])
@requires_auth
def home():
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('home.html', user_name=session_username)


@app.route('/device-details', methods=['GET', 'POST'])
@requires_auth
def device_details():
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('device_details.html', user_name=session_username)

    elif request.method == 'POST':
        device_name = request.form.get('device_name')

        device_data = collect_data_for_device(device_name)

        return render_template('device_details.html', user_name=session_username, device_name=device_name,
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
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('connections.html', user_name=session_username)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Processing....':
        searched_item = request.form.get('searched_item')
        print(searched_item)
        return render_template('connections.html', user_name=session_username)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Insert':
        local_device = request.form.get('local_device')
        local_port = request.form.get('local_port')
        remote_device = request.form.get('remote_device')
        remote_port = request.form.get('remote_port')
        interconnect_1 = request.form.get('interconnect_1')
        interconnect_2 = request.form.get('interconnect_2')

        print(local_device, local_port, remote_device, remote_port, interconnect_1, interconnect_2)
        return render_template('connections.html', user_name=session_username)


@app.route('/upload-connections', methods=['GET', 'POST'])
@requires_auth
def upload_connections():
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('upload_connections.html', user_name=session_username)
    elif request.method == 'POST' and request.form['btn_identifier'] == 'Upload Excel File' \
            and request.files:
        connections_file = request.files['file']
        connections_df = pd.read_excel(connections_file)
        connections = connections_df.to_html(classes=['table table-bordered'], header=True, index=False)
        return render_template('upload_connections.html', user_name=session_username, connections_table=connections)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Download Template':
        return send_from_directory(directory='required_files', filename='Template.xlsx', as_attachment=True)

    else:
        return render_template('upload_connections.html', user_name=session_username)


@app.route('/authentication-error', methods=['GET', 'POST'])
def authentication_required():
    return render_template('authentication_required.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
