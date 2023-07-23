import pandas as pd
import datetime
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
import boto3

def clean_questionmark(x):
    try:
        if x == "NULL":
            return None
        x = str(x).replace('?',"")
        return x 
    except Exception as e:
        print(e) 

def date_format(x):
    try: 
        if '-' in x:
            x = list(map(int, x.split('-')))
            return datetime.date(x[0],x[1],x[2])
        else:
            return datetime.datetime.strptime(x, '%B %Y %d').date()
    except: 
        return None

def convert_to_num(x, type_1):
    try:
        return type_1(x) 
    except: 
        return None 
    


class DataCleaning():
    def clean_card_data(card_data):
        card_data['card_number'] = card_data['card_number'].apply(clean_questionmark)
        card_data.loc[card_data['card_provider'] == 'NULL', 'card_provider'] = None
        return card_data.dropna()
    
    def clean_store_data(extractor):
        df_stores = extractor.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}')
        df_stores.drop('lat', inplace = True, axis = 1)
        df_stores.drop(447, inplace= True)
        df_stores['address'] = df_stores['address'].apply(lambda x: x.replace('\n', ' '))
        df_stores['longitude'] = df_stores['longitude'].apply(convert_to_num, type_1 = float)
        df_stores['latitude'] = df_stores['latitude'].apply(convert_to_num, type_1 = float)
        df_stores['staff_numbers'] = df_stores['staff_numbers'].apply(convert_to_num, type_1 = int)
        df_stores['opening_date']= df_stores['opening_date'].apply(date_format)
        for col in df_stores.columns: 
            df_stores[col] = df_stores[col].replace({'N/A': None})
        df_stores.dropna(inplace = True)
        return df_stores 







if __name__ == '__main__':
    database_connector = DatabaseConnector()
    extractor = DataExtractor()
    data_frame = DataCleaning.clean_store_data(extractor)
    database_connector.list_db_tables()
    database_connector.upload_to_db_2(data_frame, 'dim_store_details')
