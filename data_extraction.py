from database_utils import DatabaseConnector
import pandas as pd


class DataExtractor():
    def __init__(self):
        pass
    def read_rds_table(self, database_connector, table_name):
        connection = database_connector.init_db_engine()
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        data_frame = pd.DataFrame(cursor)
        return data_frame 
        
        pass 



if __name__ == '__main__':
    database_connector = DatabaseConnector()
    data_extraction = DataExtractor()

    database_connector.list_db_tables() 
    while True: 
        try:
            table_name = input("enter table name required: ")
            samuel_data = data_extraction.read_rds_table(database_connector, table_name)
            break
        except: 
            print('incorrect table name entered')
            continue

    print(samuel_data)
