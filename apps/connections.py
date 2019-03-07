from flask import render_template

from database_helper.procedures import execute_procedure
from database_helper.query import execute_query
from database_helper.sql_statements import select_all_connections


def get_connections(searched_item):
    query = select_all_connections(searched_item.lower())
    connections_df = execute_query(query)
    if connections_df.empty:
        return '''<div class="form-inline justify-content-center">
                    <h6 class="text-secondary">No data</h6>
                  </div>'''
    connections_df.columns = ['Id', 'Local Device', 'Local Port', 'Remote Device', 'Remote Port', 'Interconnect 1',
                              'Interconnect 2']
    connections_df['Edit'] = ''

    connections_df['Edit'] = connections_df['Id'].apply(
        lambda x: '<a href="/connections/edit/{}">Edit</a>'.format(x))
    connections_df.drop('Id', axis=1, inplace=True)
    connections_table = connections_df.to_html(classes=['table table-bordered'], table_id='dataTable', header=True,
                                               index=False, escape=False)

    return connections_table


def insert_single_connection(html_from_request):
    # this request object was obtained from the connection page > Insert
    # single connection form > submit
    local_device = html_from_request.get('local_device').lower()
    local_port = html_from_request.get('local_port').lower()
    remote_device = html_from_request.get('remote_device').lower()
    remote_port = html_from_request.get('remote_port').lower()
    interconnect_1 = html_from_request.get('interconnect_1').lower()
    interconnect_2 = html_from_request.get('interconnect_2').lower()

    execution_status = execute_procedure('prc_insert_manual_connection',
                                         [local_device, local_port, remote_device, remote_port, interconnect_1,
                                          interconnect_2])
    if execution_status != 'success':
        execution_status = execution_status.split(':')
        execution_status = execution_status[1].split('-')[0]
        execution_status = 'Connection Insertion Error : ' + execution_status.strip()
    return execution_status


