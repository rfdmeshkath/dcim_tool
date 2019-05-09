import cx_Oracle

from config import DATABASE_DSN, DATABASE_CREDENTIAL


def prc_test(procedure_name, parameter_list):
    dsn_string = cx_Oracle.makedsn(**DATABASE_DSN)
    DATABASE_CREDENTIAL['dsn'] = dsn_string
    connection = cx_Oracle.connect(**DATABASE_CREDENTIAL)
    cursor = connection.cursor()
    # enabling console output
    cursor.callproc("dbms_output.enable")
    cursor.execute('alter SESSION set NLS_DATE_FORMAT = \'DD-MM-YYYY HH24:MI:SS\'')
    cursor.callproc(procedure_name, parameter_list)
    statusVar = cursor.var(cx_Oracle.NUMBER)
    lineVar = cursor.var(cx_Oracle.STRING)
    # while loop for outputting oracle console output
    while True:
        cursor.callproc("dbms_output.get_line", (lineVar, statusVar))
        if statusVar.getvalue() != 0:
            break
        print(lineVar.getvalue())


if __name__ == '__main__':
    prc_test(procedure_name='', parameter_list=[])