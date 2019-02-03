import pandas as pd
from flask import Flask, render_template, request

from db_reader import get_lldp_connections

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    sesssion_username = 'Rafid'
    if request.method == 'GET':
        return render_template('home.html', user_name=sesssion_username)


@app.route('/deviceDetails', methods=['GET', 'POST'])
def device_details():
    sesssion_username = 'Rafid'
    if request.method == 'GET':
        return render_template('device_details.html', user_name=sesssion_username)

    elif request.method == 'POST':
        device_name = request.form.get('device_name')
        print(device_name)
        # conns, status = get_lldp_connections(searched_item)
        updated_time = '12 Jan 2019 12:50 am'
        connections_df = pd.read_excel('conn_test.xlsx')
        connections = connections_df.to_html(classes=['table table-bordered'], table_id='dataTable', header=True,
                                                index=False)

        cpu_x_axis = ["11:10pm", "11:15pm", "11:20pm", "11:25pm", "11:30pm", "11:35pm", "11:40pm", "11:45pm", "11:50pm", "11:55pm", "12:00pm", "12:05pm"]
        cpu_y_axis = [50, 20, 35, 90, 45, 56, 84, 33, 49, 24, 32, 98]

        ram_x_axis = ["11:10pm", "11:15pm", "11:20pm", "11:25pm", "11:30pm", "11:35pm", "11:40pm", "11:45pm", "11:50pm",
                      "11:55pm", "12:00pm", "12:05pm"]
        ram_y_axis = [110, 120, 135, 90, 145, 56, 84, 133, 49, 124, 132, 98]

        return render_template('device_details.html', user_name=sesssion_username,
                               device_name=device_name,
                               cpu_x_axis=cpu_x_axis, cpu_y_axis=cpu_y_axis,
                               ram_x_axis=ram_x_axis, ram_y_axis=ram_y_axis,
                               time=updated_time, data_table=connections)


@app.route('/connections', methods=['GET', 'POST'])
def search_connections():
    sesssion_username = 'Rafid'
    if request.method == 'GET':
        return render_template('connections.html', user_name=sesssion_username)
    elif request.method == 'POST':
        searched_item = request.form.get('searched_item')
        print(searched_item)
        return render_template('connections.html', user_name=sesssion_username)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
