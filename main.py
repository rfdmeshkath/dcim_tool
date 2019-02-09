import pandas as pd
from flask import Flask, render_template, request, send_from_directory

from device_details import collect_data_for_device

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('home.html', user_name=session_username)


@app.route('/device-details', methods=['GET', 'POST'])
def device_details():
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('device_details.html', user_name=session_username)

    elif request.method == 'POST':
        device_name = request.form.get('device_name')

        device_data = collect_data_for_device(device_name)

        return render_template('device_details.html', user_name=session_username, device_name=device_name,
                               system_namr=device_data['system_name'], os_details=device_data['os_details'],
                               up_time=device_data['up_time'], total_ram=device_data['total_ram'],
                               cpu_x_axis=device_data['memory_timeline'], cpu_y_axis=device_data['cpu_usages'],
                               cpu_last_updated=device_data['memory_last_updated'],
                               ram_x_axis=device_data['memory_timeline'], ram_y_axis=device_data['ram_usages'],
                               ram_last_updated=device_data['memory_last_updated'],
                               data_table=device_data['lldp_connections_table'], lldp_last_updated=device_data['lldp_last_updated'])


@app.route('/connections', methods=['GET', 'POST'])
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
def upload_connections():
    session_username = 'Rafid'
    if request.method == 'GET':
        return render_template('upload_connections.html', user_name=session_username)
    elif request.method == 'POST' and request.form['btn_identifier'] == 'Upload Excel File' \
            and request.files:
        connections_file = request.files['file']
        connections_df = pd.read_excel(connections_file)
        connections = connections_df.to_html(classes=['table table-bordered'], header=True,
                                             index=False)
        return render_template('upload_connections.html', user_name=session_username, connections_table=connections)

    elif request.method == 'POST' and request.form['btn_identifier'] == 'Download Template':
        return send_from_directory(directory='required_files', filename='Template.xlsx', as_attachment=True)

    else:
        return render_template('upload_connections.html', user_name=session_username)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
