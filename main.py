from flask import Flask, render_template, request

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
        return render_template('connections.html', user_name=sesssion_username)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
