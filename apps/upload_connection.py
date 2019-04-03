import pandas as pd
import numpy as np

from database_helper.procedures import execute_procedure


def file_error_check(file):
    empty_df = pd.DataFrame()
    columns_expected_in_file = ['Local Device', 'Local Port', 'Remote Device', 'Remote Port', 'Interconnect 1',
                                'Interconnect 2']

    # check if its a excel file or not
    if 'xlsx' not in file.filename:
        return 'Excel template file is required', empty_df

    connections_df = pd.read_excel(file)
    connections_df = connections_df.replace(np.nan, '', regex=True)

    # check if it is the right excel file
    if connections_df.columns.tolist() != columns_expected_in_file:
        return 'Wrong template file', empty_df

    # check different fields in the excel file
    for index, row in connections_df.iterrows():
        if row['Local Device'] == '':
            return 'Local Device missing in row {}'.format(index + 1), empty_df
        if row['Local Port'] == '':
            return 'Local Port missing in row {}'.format(index + 1), empty_df
        if row['Remote Device'] == '':
            return 'Remote Device missing in row {}'.format(index + 1), empty_df
        if row['Remote Port'] == '':
            return 'Remote Port missing in row {}'.format(index + 1), empty_df
        if row['Local Device'] == row['Remote Device']:
            return 'Local and Remote device can not be same in row {}'.format(index + 1), empty_df

    connections_df.to_csv('./required_files\connections.csv', sep=',', index=False)
    return 'success', connections_df


def multiple_connection_insert():
    connections_df = pd.read_csv('./required_files\connections.csv', sep=',')
    success_list = []
    error_list = []
    for index, row in connections_df.iterrows():
        prc_params = [row['Local Device'], row['Local Port'], row['Remote Device'], row['Remote Port'],
                      row['Interconnect 1'], row['Interconnect 2']]
        execution_status = execute_procedure('prc_insert_manual_connection', prc_params)
        if execution_status == 'success':
            success_list.append(prc_params)
        else:
            error_list.append(prc_params)

    column_names = ['Local Device', 'Local Port', 'Remote Device', 'Remote Port', 'Interconnect 1', 'Interconnect 2']
    success_df = pd.DataFrame(success_list, columns=column_names)
    error_df = pd.DataFrame(error_list, columns=column_names)

    success_table = ''
    error_table = ''
    if not success_df.empty:
        success_table = success_df.to_html(classes=['table table-bordered'], header=True, index=False, na_rep='')
    if not error_df.empty:
        error_table = error_df.to_html(classes=['table table-bordered'], header=True, index=False, na_rep='')
    return success_table, error_table
