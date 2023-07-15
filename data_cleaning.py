import pandas as pd
import datetime
from database_utils import DatabaseConnector
from data_extraction import DataExtractor

def clean_questionmark(x):
    try:
        if x == "NULL":
            return None
        x = str(x).replace('?',"")
        return x 
    except Exception as e:
        print(e) 

class DataCleaning():
    def clean_card_data(card_data):
        card_data['card_number'] = card_data['card_number'].apply(clean_questionmark)
        card_data.loc[card_data['card_provider'] == 'NULL', 'card_provider'] = None
        return card_data.dropna()
    pass

if __name__ == '__main__':
    database_connector = DatabaseConnector()
    extractor = DataExtractor('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
    data_frame = extractor.retrieve_pdf_data()
    data_frame = DataCleaning.clean_card_data(data_frame)
    database_connector.list_db_tables()
    database_connector.upload_to_db_2(data_frame, 'dim_card_details')