from database_utils import DatabaseConnector
import pandas as pd
import tabula
import datetime


class DataExtractor():
    def __init__(self, pdf_url):
        self.pdf_url = pdf_url
        
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


    def extract_pdf(self):
        df = pd.concat(tabula.read_pdf(self.pdf_url, pages = 'all'))
        df['date_payment_confirmed'] = df['date_payment_confirmed'].apply(self.to_date)
        df['expiry_date'] = pd.to_datetime(df['expiry_date'],format = '%m/%d',errors= 'coerce').dt.date
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
    data_frame = extractor.extract_pdf()
    database_connector.list_db_tables()
    database_connector.upload_to_db_2(data_frame)