import pandas as pd


def file_error_check(file):
    columns_expected_in_file = ['Local Device', 'Local Port', 'Remote Device', 'Remote Port', 'Interconnect 1',
                                'Interconnect 2']
    if 'xlsx' not in file.filename:
        return 'Excel template file is required'
    connections_df = pd.read_excel(file)
    if connections_df.columns.tolist() != columns_expected_in_file:
        return 'Wrong template file'
    for index, row in connections_df.iterrows():
        if row['Local Device'] == '' or row['Local Port'] == '' \
                or row['Remote Device'] == '' and row['Remote Port'] == '':
            return 'Field missing in row {}'.format(index + 1)
    print(connections_df)
