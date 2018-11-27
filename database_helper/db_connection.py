import cx_Oracle

from config import DATABASE_CREDENTIAL, DATABASE_DSN


def db_connect(dsn, authentication):
    try:
        dsn_string = cx_Oracle.makedsn(**dsn)
        DATABASE_CREDENTIAL['dsn'] = dsn_string
        connection = cx_Oracle.connect(**authentication)
        cursor = connection.cursor()
    except Exception as e:
        connection = 'Error-501: Database connection error'
        cursor = str(e)
        print(str(e))
    return connection, cursor


connection,cursor = db_connect(DATABASE_DSN, DATABASE_CREDENTIAL)
temp_var = cursor.execute('select * from connections')

result = temp_var.fetchall()

print(result, type(result))
cursor.close()
connection.close()
