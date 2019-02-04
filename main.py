import os

from flask import Flask, render_template, request, send_file, send_from_directory
import pandas as pd

from db_reader import get_lldp_connections

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
        print(device_name)
        # conns, status = get_lldp_connections(searched_item)
        updated_time = '12 Jan 2019 12:50 am'
        connections_df = pd.read_excel('conn_test.xlsx')
        connections = connections_df.to_html(classes=['table table-bordered'], table_id='dataTable', header=True,
                                             index=False)

        cpu_x_axis = ["11:10pm", "11:15pm", "11:20pm", "11:25pm", "11:30pm", "11:35pm", "11:40pm", "11:45pm", "11:50pm",
                      "11:55pm", "12:00pm", "12:05pm"]
        cpu_y_axis = [50, 20, 35, 90, 45, 56, 84, 33, 49, 24, 32, 98]

        ram_x_axis = ["11:10pm", "11:15pm", "11:20pm", "11:25pm", "11:30pm", "11:35pm", "11:40pm", "11:45pm", "11:50pm",
                      "11:55pm", "12:00pm", "12:05pm"]
        ram_y_axis = [110, 120, 135, 90, 145, 56, 84, 133, 49, 124, 132, 98]

        return render_template('device_details.html', user_name=session_username,
                               device_name=device_name,
                               cpu_x_axis=cpu_x_axis, cpu_y_axis=cpu_y_axis,
                               ram_x_axis=ram_x_axis, ram_y_axis=ram_y_axis,
                               time=updated_time, data_table=connections)


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
