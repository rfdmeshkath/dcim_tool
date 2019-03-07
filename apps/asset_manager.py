from required_files.rf_code_mock_api import api
import pandas as pd


def get_api_data():
    api_data = api
    asset_df = pd.DataFrame(api_data['results'])
    print(asset_df)


get_api_data()
