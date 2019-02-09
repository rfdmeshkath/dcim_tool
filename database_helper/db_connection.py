import cx_Oracle

from config import DATABASE_CREDENTIAL, DATABASE_DSN, ERROR_MESSAGES


def db_connect():
    try:
        dsn_string = cx_Oracle.makedsn(**DATABASE_DSN)
        DATABASE_CREDENTIAL['dsn'] = dsn_string
        connection = cx_Oracle.connect(**DATABASE_CREDENTIAL)
        cursor = connection.cursor()
    except Exception as e:
        connection = ERROR_MESSAGES['database_connection_error']
        cursor = str(e)
    return connection, cursor
