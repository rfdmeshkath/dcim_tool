import cx_Oracle


connection_details = {
    'host': 'localhost',
    'port': '1521',
    'sid': 'xe',
    'username': '',
    'password': '',
}


def db_connect(connection_details):
    try:
        dsn_string = cx_Oracle.makedsn('localhost', '1521', 'xe')
        connection = cx_Oracle.connect(user='fyp_project', password='fyp_project', dsn=dsn_string)
        cursor = connection.cursor()
    except Exception as e:
        connection = 'Error-501: Database connection error'
        cursor = str(e)
    return connection, cursor


connection,cursor = db_connect('aaa')
temp_var = cursor.execute('select sysdate from dual')

result = temp_var.fetchall()

print(result, type(result))
cursor.close()
connection.close()
