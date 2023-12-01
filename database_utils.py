import yaml
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import datetime
import psycopg2


def get_type(col_type):
    if 'str' in str(col_type):
        return 'VARCHAR(225)'
    elif 'float' in str(col_type):
        return 'FLOAT'
    elif 'int' in str(col_type): 
        return 'VARCHAR(225)'
    elif 'date' in str(col_type):
        return 'DATE'
    else: 
        return 'VARCHAR(225)'
    


class DatabaseConnector():
    def __init__(self, cred_file = 'db_creds.yaml'): 
        self.cred_file = cred_file 

    def read_db_creds(self):
        print('reading credentials...')
        with open(self.cred_file) as file:
            cred = yaml.safe_load(file)
        return cred
    
    def init_db_engine(self):
        cred = self.read_db_creds()
        print('connecting to the database....')
        connection = mysql.connector.connect(host = cred['RDS_HOST'] , 
                                     user = cred['RDS_USER'], 
                                     password = cred['RDS_PASSWORD'] ,
                                     port = str(cred['RDS_PORT']),
                                     database = cred['RDS_DATABASE'])
        return connection 
    

    def list_db_tables(self):
        connection = self.init_db_engine() 
        cursor = connection.cursor() 
        print('reading existing tables....')
        cursor.execute('SHOW TABLES')
        for row in cursor:
            print(row)
    
    # def upload_to_db(self, pd_dataframe):
    #     cred = self.read_db_creds()
    #     db_url = f'mysql+mysqlconnector://{cred["RDS_USER"]}:{cred["RDS_PASSWORD"]}@{cred["RDS_HOST"]}/{cred["RDS_DATABASE"]}'
    #     engine = create_engine(db_url)
    #     data_columns = pd_dataframe.columns
    #     with engine.connect() as connection:
    #         connection.execute(f"""CREATE TABLE IF NOT EXISTS dim_users(
    #                            {data_columns[0]} VARCHAR(100),
    #                              {data_columns[1]} DATE,
    #                                {data_columns[2]} VARCHAR(100),
    #                                  {data_columns[3]} DATE)""")
    
    
    
    def upload_to_db_2(self, pd_dataframe, table_name):
        connection = self.init_db_engine() 
        cursor = connection.cursor() 
        data_columns = pd_dataframe.columns
        insert_query = f'CREATE TABLE IF NOT EXISTS {table_name}('
        for col in data_columns:
            insert_query += f'{col} {get_type(type(pd_dataframe[col].iloc[0]))},'
        insert_query = insert_query[:-1] + ')'
        print(insert_query)
        cursor.execute(insert_query)
        cursor.close()
        
        cred = self.read_db_creds()
        db_url = f'mysql+mysqlconnector://{cred["RDS_USER"]}:{cred["RDS_PASSWORD"]}@{cred["RDS_HOST"]}/{cred["RDS_DATABASE"]}'
        engine = create_engine(db_url)
        pd_dataframe.to_sql(table_name,con = engine, if_exists = 'append', index = False)


"--------------------------------------------------------------------------------------------------------------------------------------"

class DatabaseConnector_postgres():
    def __init__(self, cred_file = 'db_creds_2.yaml'): 
        self.cred_file = cred_file 

    def read_db_creds(self):
        print('reading credentials...')
        with open(self.cred_file) as file:
            cred = yaml.safe_load(file)
        return cred
    
    def init_db_engine(self):
        cred = self.read_db_creds()
        print('connecting to the database....')
        connection = psycopg2.connect(host = cred['RDS_HOST'] , 
                                     user = cred['RDS_USER'], 
                                     password = cred['RDS_PASSWORD'] ,
                                     port = str(cred['RDS_PORT']),
                                     dbname= cred['RDS_DATABASE'])
        return connection 
    

    def list_db_tables(self):
        connection = self.init_db_engine() 
        print('reading existing tables....')
        query = """
        SELECT tablename FROM pg_catalog.pg_tables 
        WHERE schemaname != 'pg_catalog' AND 
        schemaname != 'information_schema';
        """
        existing_tables = pd.read_sql(query, connection)
        return existing_tables
        
    
    # def upload_to_db(self, pd_dataframe):
    #     cred = self.read_db_creds()
    #     db_url = f'mysql+mysqlconnector://{cred["RDS_USER"]}:{cred["RDS_PASSWORD"]}@{cred["RDS_HOST"]}/{cred["RDS_DATABASE"]}'
    #     engine = create_engine(db_url)
    #     data_columns = pd_dataframe.columns
    #     with engine.connect() as connection:
    #         connection.execute(f"""CREATE TABLE IF NOT EXISTS dim_users(
    #                            {data_columns[0]} VARCHAR(100),
    #                              {data_columns[1]} DATE,
    #                                {data_columns[2]} VARCHAR(100),
    #                                  {data_columns[3]} DATE)""")
    
    
    
    def upload_to_db_2(self, pd_dataframe, table_name):
        connection = self.init_db_engine() 
        cursor = connection.cursor() 
        data_columns = pd_dataframe.columns
        insert_query = f'CREATE TABLE IF NOT EXISTS {table_name}('
        for col in data_columns:
            insert_query += f'{col} {get_type(type(pd_dataframe[col].iloc[0]))},'
        insert_query = insert_query[:-1] + ')'
        print(insert_query)
        cursor.execute(insert_query)
        cursor.close()
        
        cred = self.read_db_creds()
        db_url = f'mysql+mysqlconnector://{cred["RDS_USER"]}:{cred["RDS_PASSWORD"]}@{cred["RDS_HOST"]}/{cred["RDS_DATABASE"]}'
        engine = create_engine(db_url)
        pd_dataframe.to_sql(table_name,con = engine, if_exists = 'append', index = False)




    




