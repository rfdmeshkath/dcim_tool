from config import ERROR_MESSAGES
from database_helper.db_connection import db_connect


def execute_procedure(procedure_name, param_list):
    connection, cursor = db_connect()

    if connection == ERROR_MESSAGES['database_connection_error']:
        return ERROR_MESSAGES['database_connection_error'] + ' - ' + cursor

    try:
        cursor.execute('alter SESSION set NLS_DATE_FORMAT = \'DD-MM-YYYY HH24:MI:SS\'')
        cursor.callproc(procedure_name, param_list)
        return 'success'

    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        connection.close()

