import pandas as pd
import datetime
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
import boto3
import yaml

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


def clean_money(x):
    if type(x) == float:
        return x 
    if '£' in x: 
        return float(x.replace('£', ''))
    else: 
        return None 

def clean_weights(x):
    if type(x) == float:
        return x 
    elif 'kg' in x:
        return float(x.replace('kg', ''))*1000
    elif 'ml' in x: 
        return float(x.replace('ml', ''))
    elif x.isnumeric():
        return float(x)   
    elif 'g' in x:
        if 'x' in x:
            x = x.replace('g', '').replace(' ', '')
            x = x.split('x')
            result = 1 
            for item in x: 
                result = result * float(item)
            return result 
        return float(x.replace('g', '').replace(' ', ''))
    elif 'oz' in x:
        return float(x.replace('oz', ''))*28.35
    else: 
        print(x) 
        return None



class DataCleaning():
    def read_s3_creds():
        print('reading credentials...')
        with open('db_creds.yaml') as file:
            cred = yaml.safe_load(file)
        return cred
    
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
    
    def clean_user_data(df_users):
        df_users['address'] = df_users['address'].apply(lambda x: x.replace('\n', ' '))
        df_users['date_of_birth']= df_users['date_of_birth'].apply(date_format)
        df_users['join_date']= df_users['join_date'].apply(date_format)
        for col in df_users.columns: 
            df_users[col] = df_users[col].replace({'N/A': None})
        df_users.dropna(inplace = True)
        return df_users 

    def clean_orders_data(df_tables):
        df_tables = df_tables.drop(['first_name', 'last_name','index', '1'], axis = 1)
        return df_tables


    def convert_product_weights(df):
        df['weight'] = df['weight'].apply(clean_weights)
        return df

    def clean_products_data(df):
        df['product_price'] = df['product_price'].apply(clean_money)
        df['date_added'] = df['date_added'].apply(date_format)
        df.dropna(inplace = True)
        return df
    
    def extract_from_s3(path = 's3://data-handling-public/products.csv'): 
        bucket = path.split('/')[-2]
        key = path.split('/')[-1]
        cred = DataCleaning.read_s3_creds()
        s3 = boto3.client('s3', region_name = 'eu-west-1', aws_access_key_id = cred['aws_access_key_id'], aws_secret_access_key = cred['aws_secret_access_key'])
        obj = s3.get_object(Bucket = bucket, Key =  key)
        return pd.read_csv(obj['Body'], index_col = 0) 




if __name__ == '__main__':
    database_connector = DatabaseConnector()
    extractor = DataExtractor()
    # data_frame = DataCleaning.clean_store_data(extractor)
    # database_connector.list_db_tables()
    # database_connector.upload_to_db_2(data_frame, 'dim_store_details')
    df_products = DataCleaning.extract_from_s3()
    df_products = DataCleaning.convert_product_weights(df_products)
    df_products = DataCleaning.clean_products_data(df_products)
    print(df_products.removed.unique())
    # database_connector.list_db_tables()
    # database_connector.upload_to_db_2(df_products, 'dim_products')


