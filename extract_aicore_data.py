from data_extraction import *
from data_cleaning import *
from database_utils import *


if __name__ == '__main__':
    database_connector = DatabaseConnector_postgres()
    existing_tables = database_connector.list_db_tables()
    print(existing_tables)
    data_extractor = DataExtractor()
    table_data = data_extractor.read_rds_tables_postgress(database_connector).iloc[:,1:]
    table_data = DataCleaning.clean_user_data(table_data)

    database_connector = DatabaseConnector()
    database_connector.list_db_tables()
    database_connector.upload_to_db_2(table_data, 'dim_users')



