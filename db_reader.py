from database_helper.db_connection import db_connect
import pandas as pd


def get_lldp_connections(searched_item):
    conns_statement = '''select * from connections where local_device like \'%{}%\''''.format(searched_item.upper())
    stat_statement = '''select * from device_status where device_name like \'%{}%\''''.format(searched_item.upper())
    connection, cursor = db_connect()
    db_connections = cursor.execute(conns_statement).fetchall()
    db_status = cursor.execute(stat_statement).fetchall()
    cursor.close()
    connection.close()
    db_connections = pd.DataFrame(db_connections, columns=['connection ID', 'Local Device', 'Local Port',
                                                           'Remote device', 'Remote Port', 'Date', 'Time'])
    db_status = pd.DataFrame(db_status, columns=['Status ID', 'Device Name', 'Total Ram (MB)', 'Used (MB)', 'Free (MB)',
                                                 'CPU Usage %', 'Date', 'Time'])

    db_connections = db_connections.to_html(classes=['table responsive table-togglable table-hover'], header=True,
                                            index=False, table_id='DataTable_0')

    db_status = db_status.to_html(classes=['table responsive table-togglable table-hover'], header=True,
                                  index=False, table_id='DataTable_1')

    return db_connections, db_status

