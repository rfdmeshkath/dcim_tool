import pandas as pd

from config import ERROR_MESSAGES
from database_helper.db_connection import db_connect


def execute_query(select_statement):
    connection, cursor = db_connect()

    if connection == ERROR_MESSAGES['database_connection_error']:
        return ERROR_MESSAGES['database_connection_error'] + ' - ' + cursor

    data_df = pd.DataFrame()

    try:
        cursor.execute('ALTER SESSION SET NLS_DATE_FORMAT = \'DD-MM-YYYY HH24:MI:SS\'')
        db_data = cursor.execute(select_statement)
        data_df = pd.DataFrame(db_data.fetchall())
        data_df = data_df.fillna('')

    except Exception as e:
        print('error logging will go here ' + str(e))

    finally:
        cursor.close()
        connection.close()
        return data_df

