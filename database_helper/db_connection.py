import cx_Oracle


dsn_string = cx_Oracle.makedsn('localhost', '1521', 'xe')
connection = cx_Oracle.connect(user='fyp_project', password='fyp_project', dsn=dsn_string)

print(connection.version)

cursor = connection.cursor()

temp_var = cursor.execute('select sysdate from dual')

result = temp_var.fetchall()

print(result, type(result))
cursor.close()
connection.close()
