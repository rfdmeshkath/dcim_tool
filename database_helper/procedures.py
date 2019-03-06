from config import ERROR_MESSAGES
from database_helper.db_connection import db_connect
import cx_Oracle


def execute_procedure(procedure_name, param_list):
    connection, cursor = db_connect()

    if connection == ERROR_MESSAGES['database_connection_error']:
        return ERROR_MESSAGES['database_connection_error'] + ' - ' + cursor

    try:
        cursor.callproc("dbms_output.enable")
        cursor.execute('alter SESSION set NLS_DATE_FORMAT = \'DD-MM-YYYY HH24:MI:SS\'')
        cursor.callproc(procedure_name, param_list)
        statusVar = cursor.var(cx_Oracle.NUMBER)
        lineVar = cursor.var(cx_Oracle.STRING)
        while True:
            cursor.callproc("dbms_output.get_line", (lineVar, statusVar))
            if statusVar.getvalue() != 0:
                break
            print(lineVar.getvalue())
        return 'success'

    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        connection.close()

