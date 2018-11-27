import cx_Oracle

from config import DATABASE_CREDENTIAL, DATABASE_DSN


def db_connect():
    try:
        dsn_string = cx_Oracle.makedsn(**DATABASE_DSN)
        DATABASE_CREDENTIAL['dsn'] = dsn_string
        connection = cx_Oracle.connect(**DATABASE_CREDENTIAL)
        cursor = connection.cursor()
    except Exception as e:
        connection = 'Error-501: Database connection error'
        cursor = str(e)
        print(str(e))
    return connection, cursor


# connection,cursor = db_connect()
# temp_var = cursor.execute('select * from connections')
#
# result = temp_var.fetchall()
#
# print(result, type(result))
# cursor.close()
# connection.close()
