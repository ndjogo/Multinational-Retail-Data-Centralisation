import pandas as pd 
from data_cleaning import convert_to_num
from database_utils import DatabaseConnector

def convert_time(x):
    if ':' not in x: 
        return 0
    else: 
        return x




link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'

date_data = pd.read_json(link)


date_data['timestamp'] = pd.to_datetime(date_data['timestamp'].apply(convert_time)).dt.time

date_data['month'] = date_data['month'].apply(convert_to_num, type_1 = int)
date_data['year'] = date_data['year'].apply(convert_to_num, type_1 = int)
date_data['day'] = date_data['day'].apply(convert_to_num, type_1 = int)

date_data.dropna(inplace = True)

date_data['year'] = date_data['year'].astype(int, errors = 'ignore')
date_data['month'] = date_data['month'].astype(int, errors = 'ignore')
date_data['day'] = date_data['day'].astype(int, errors = 'ignore')

database_connector = DatabaseConnector()
database_connector.list_db_tables()
database_connector.upload_to_db_2(date_data, 'dim_date_times')
