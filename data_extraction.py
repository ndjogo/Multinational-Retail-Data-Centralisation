from database_utils import DatabaseConnector
import pandas as pd
import tabula
import datetime
import requests 

def to_date(x):
    try:
        x = list(map(int, x.split('-')))
        date = datetime.date(x[0],x[1],x[2])
    except Exception as e:
        print(e) 
        date = None

    return date



class DataExtractor():
    def __init__(self, pdf_url):
        self.pdf_url = pdf_url
        self.header_dict = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX' }
        
    def read_rds_table(self, database_connector, table_name):
        connection = database_connector.init_db_engine()
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        data_frame = pd.DataFrame(cursor)
        return data_frame 
    
    def to_date(self, x):
        try:
            x = list(map(int, x.split('-')))
            date = datetime.date(x[0],x[1],x[2])
        except Exception as e:
            print(e) 
            date = None

        return date
    
    def retrieve_pdf_data(self):
        pdf_url = self.pdf_url 
        df = pd.concat(tabula.read_pdf(pdf_url, pages = 'all'))
        df['date_payment_confirmed'] = df['date_payment_confirmed'].apply(to_date)
        df['expiry_date'] = pd.to_datetime(df['expiry_date'],format = '%m/%y',errors= 'coerce').dt.date
        return df
    
    def list_number_of_stores(self,end_point):
        response = requests.get(end_point, headers = self.header_dict)
        number_stores = response.json()
        return number_stores['number_stores'] 
    
    def retrieve_stores_data(self,end_point):
        store_numbers = self.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores')
        df = pd.DataFrame()
        for store_number in range(store_numbers): 
            store_point_i = end_point.replace('{store_number}', str(store_number))
            response = requests.get(store_point_i, headers = self.header_dict)
            store_data = response.json() 
            df = pd.concat([df, pd.DataFrame(store_data, index = [0])], ignore_index = True)
        df.set_index('index', drop = True, inplace= True)
        return df
        




# if __name__ == '__main__':
#     database_connector = DatabaseConnector()
#     data_extraction = DataExtractor()

#     database_connector.list_db_tables() 
#     while True: 
#         try:
#             table_name = input("enter table name required: ")
#             samuel_data = data_extraction.read_rds_table(database_connector, table_name)
#             break
#         except: 
#             print('incorrect table name entered')
#             continue

#     print(samuel_data)


if __name__ == '__main__':
    database_connector = DatabaseConnector()
    extractor = DataExtractor('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
    data_frame = extractor.retrieve_pdf_data()
    database_connector.list_db_tables()
    database_connector.upload_to_db_2(data_frame, 'dim_users')