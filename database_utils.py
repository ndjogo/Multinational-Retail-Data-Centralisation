import yaml
import mysql.connector

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
    
 

    pass


if __name__ == '__main__':
    database_connector = DatabaseConnector()
    database_connector.list_db_tables()


