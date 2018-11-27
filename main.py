from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    sesssion_username = 'Rafid'
    if request.method == 'GET':
        return render_template('home.html', user_name=sesssion_username)


@app.route('/connections', methods=['GET', 'POST'])
def search_connections():
    sesssion_username = 'Rafid'
    if request.method == 'GET':
        return render_template('connections.html', user_name=sesssion_username)


    elif request.method == 'POST':
        searched_item = request.form.get('searched_item')
        print(searched_item), type(searched_item)
        data = pd.read_excel('test.xlsx', index=False)
        data = data.to_html(classes=['table table-striped'], header=True, index=False, table_id='DataTable_0')
        return render_template('tables.html', user_name=sesssion_username, data_table=data, escape=False)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
