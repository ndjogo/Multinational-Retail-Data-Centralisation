# Multinational Retail Data Centralisation

# Table of Contents, if the README file is long

# A description of the project: what it does, the aim of the project, and what you learned
## In this project we are collecting data from multiple sources (pdf table, json file and S3). For every data source, we cleaned the data and the uploaded it to Amazon postgres database online. 


# Installation instructions

To install MySQL, you can follow these general steps. Please note that the exact steps may vary depending on your operating system. I'll provide instructions for some common operating systems: Windows, macOS, and Ubuntu (Linux).

### Windows:

1. **Download MySQL Installer:**
   - Visit the MySQL Community Downloads page: https://dev.mysql.com/downloads/installer/
   - Choose the MySQL Installer for Windows.

2. **Install MySQL Installer:**
   - Run the installer you downloaded.
   - Choose "Custom" installation type.

3. **Select Products:**
   - In the product selection, choose "MySQL Server" and other components you may need (e.g., MySQL Workbench, MySQL Shell).

4. **Configuration:**
   - Follow the installation wizard, which will guide you through configuring MySQL Server.
   - Set a root password for MySQL.

5. **Complete Installation:**
   - Continue with the installation process, and it will install MySQL and the selected components.

6. **Start MySQL:**
   - After installation, start MySQL Server using the MySQL Workbench or the Windows Services Manager.

### macOS (Using Homebrew):

1. **Install Homebrew (if not already installed):**
   - Open Terminal.
   - Run the following command to install Homebrew if you haven't already:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

2. **Install MySQL:**
   - Run the following command to install MySQL:
     ```
     brew install mysql
     ```

3. **Start MySQL:**
   - After installation, start MySQL using the following command:
     ```
     brew services start mysql
     ```

### Ubuntu (Linux):

1. **Update Package List:**
   - Open a terminal.
   - Update the package list to ensure you have the latest information about available packages:
     ```
     sudo apt update
     ```

2. **Install MySQL Server:**
   - Install MySQL Server and the client by running:
     ```
     sudo apt install mysql-server
     ```

3. **Secure MySQL Installation:**
   - During installation, you will be prompted to set the root password for MySQL. Make sure to set a strong password.
   - Run the following command to secure your installation further:
     ```
     sudo mysql_secure_installation
     ```

4. **Start MySQL:**
   - After installation, MySQL should start automatically. You can check its status with:
     ```
     sudo systemctl status mysql
     ```

# Code File Structure

### Data Cleaning Python Script

This Python script, `data_cleaning.py`, is designed to clean and preprocess data collected from various sources, including an online PDF file, a JSON file, and an S3 location. Below is an explanation of each function within the script:

#### Importing Libraries
- The script imports necessary libraries such as `pandas`, `datetime`, `yaml`, `boto3`, and custom modules (`DatabaseConnector` and `DataExtractor`) for data handling and processing.

#### Data Cleaning Functions
1. `clean_questionmark(x)`: This function removes question marks from the input string `x`. It also handles cases where the input is "NULL" and returns None in such cases.

2. `date_format(x)`: This function formats the date string `x` into a `datetime.date` object. It handles two date formats - one with hyphens and one with month name, year, and day.

3. `convert_to_num(x, type_1)`: This function attempts to convert the input `x` to a numeric type specified by `type_1`.

4. `clean_money(x)`: This function cleans monetary values by removing the pound sign and converting the string to a float.

5. `clean_weights(x)`: This function cleans weight values by converting them to a consistent unit (grams). It handles various formats including kilograms, milliliters, ounces, and numeric values.

#### DataCleaning Class
- This class contains methods for cleaning different types of data:

1. `read_s3_creds()`: This method reads AWS credentials from a YAML file (`db_creds.yaml`).

2. `clean_card_data(card_data)`: Cleans card data by applying the `clean_questionmark` function to the 'card_number' column and dropping rows with missing card numbers.

3. `clean_country_code(country_code)`: Cleans country codes by ensuring they are not longer than 4 characters.

4. `clean_store_data(extractor)`: Cleans store data retrieved using the `DataExtractor` object. It drops unnecessary columns, formats addresses, converts data types, handles missing values, and ensures data integrity.

5. `clean_user_data(df_users)`: Cleans user data by formatting addresses, dates, handling missing values, and ensuring data integrity.

6. `clean_orders_data(df_tables)`: Cleans order data by dropping unnecessary columns.

7. `convert_product_weights(df)`: Converts product weights to a consistent unit (grams).

8. `clean_products_data(df)`: Cleans product data by formatting prices, dates, handling missing values, and ensuring data integrity.

9. `extract_from_s3(path)`: Extracts data from an S3 path specified. It reads credentials, connects to S3, retrieves the file, and returns a DataFrame.

#### Main Function
- In the main block, an instance of `DatabaseConnector` and `DataExtractor` is created. Store data is cleaned, uploaded to the database, and the tables are listed.

### Running the Script
To execute the script, ensure that all necessary dependencies are installed and provide appropriate input data paths. Run the script using a Python interpreter.

```python
python data_cleaning.py
```

### Data Extraction Python Script

The Python script `data_extraction.py` is responsible for extracting data from various sources, including PDF files and API endpoints. Here's a breakdown of the code:

#### Importing Libraries
- The script imports necessary libraries such as `pandas`, `tabula`, `datetime`, `requests`, and `yaml` for data extraction and handling.

#### DataExtractor Class
- This class contains methods for extracting data from different sources:

1. `__init__(self, pdf_url=None)`: Initializes the DataExtractor object with an optional PDF URL and reads API credentials from a YAML file (`db_creds_2.yaml`).

2. `to_date(self, x)`: Converts a date string `x` into a `datetime.date` object.

3. `read_rds_table(self, database_connector, table_name)`: Reads data from a specified table in the RDS database using the provided `DatabaseConnector` object.

4. `retrieve_pdf_data(self)`: Retrieves data from a PDF file specified by the `pdf_url`. It uses `tabula` to read tables from PDF pages, converts date formats, and returns a DataFrame.

5. `list_number_of_stores(self, end_point)`: Retrieves the number of stores from a specified API endpoint using a GET request.

6. `retrieve_stores_data(self, end_point)`: Retrieves store data from multiple API endpoints by iterating over store numbers, sending GET requests, and concatenating the results into a DataFrame.

7. `read_rds_tables_postgress(self, connector)`: Reads data from a specified table in the PostgreSQL database using the provided `DatabaseConnector` object.

#### Main Function (Commented Out)
- The main block contains commented-out code that demonstrates how to use the `DatabaseConnector` and `DataExtractor` objects to retrieve, clean, and upload data to the database.

### Running the Script
To execute the script, ensure that all necessary dependencies are installed and provide appropriate input data paths or API endpoints. Uncomment the desired code blocks in the main function to run specific functionalities.

```python
python data_extraction.py
```

### Database Utility Python Script

The Python script `database_utils.py` provides utility functions to interact with databases, including MySQL and PostgreSQL. Below is an explanation of the code:

#### Importing Libraries
- The script imports necessary libraries such as `yaml`, `mysql.connector`, `psycopg2`, `pandas`, `datetime`, and `sqlalchemy` for database connection and management.

#### DatabaseConnector Class (MySQL)
- This class contains methods for interacting with a MySQL database:

1. `__init__(self, cred_file='db_creds.yaml')`: Initializes the DatabaseConnector object with an optional credentials file (`db_creds.yaml` by default).

2. `read_db_creds(self)`: Reads database credentials from the specified credentials file.

3. `init_db_engine(self)`: Initializes a connection to the MySQL database using the credentials read from the file.

4. `list_db_tables(self)`: Retrieves and prints the names of existing tables in the connected MySQL database.

5. `upload_to_db_2(self, pd_dataframe, table_name)`: Creates a new table in the database with the specified name if it doesn't exist and uploads the DataFrame `pd_dataframe` to the table.

#### DatabaseConnector_postgres Class (PostgreSQL)
- This class contains similar methods as the DatabaseConnector class but is tailored for PostgreSQL databases:

1. `__init__(self, cred_file='db_creds_2.yaml')`: Initializes the DatabaseConnector_postgres object with an optional credentials file (`db_creds_2.yaml` by default) specific for PostgreSQL.

2. `read_db_creds(self)`: Reads database credentials from the specified credentials file.

3. `init_db_engine(self)`: Initializes a connection to the PostgreSQL database using the credentials read from the file.

4. `list_db_tables(self)`: Retrieves and returns a DataFrame containing the names of existing tables in the connected PostgreSQL database.

5. `upload_to_db_2(self, pd_dataframe, table_name)`: Creates a new table in the database with the specified name if it doesn't exist and uploads the DataFrame `pd_dataframe` to the table.

#### Supporting Functions
- `get_type(col_type)`: Returns the SQL data type based on the Python data type of a column in a DataFrame.

### Running the Script
To execute the script, ensure that all necessary dependencies are installed and provide appropriate input data paths or API endpoints. You can create instances of the `DatabaseConnector` or `DatabaseConnector_postgres` class and call the methods as needed.


### Date Data Upload Python Script

The Python script `date_data_upload.py` is responsible for uploading date-related data to a database after performing some preprocessing. Here's a breakdown of the code:

#### Importing Libraries
- The script imports necessary libraries such as `pandas` and custom modules (`data_cleaning`, `DatabaseConnector`) for data manipulation and database interaction.

#### Supporting Function
- `convert_time(x)`: Converts time strings to time objects. If the input string does not contain a colon (':'), it returns 0; otherwise, it returns the time object.

#### Main Function
1. **Data Retrieval and Preprocessing**:
    - Data is retrieved from a JSON file hosted at the specified link and stored in a DataFrame (`date_data`).
    - The DataFrame is converted to a CSV file named `test_timestamp.csv`.
    - Time strings in the 'timestamp' column are converted to time objects using the `convert_time` function and stored back in the DataFrame. The updated DataFrame is saved to a CSV file named `test_timestamp_updated.csv`.
    - The data types of 'month', 'year', and 'day' columns are converted to integers using the `convert_to_num` function from the `data_cleaning` module.
    - NaN values are dropped from the DataFrame.

2. **Database Interaction**:
    - An instance of the `DatabaseConnector` class is created.
    - Existing tables in the database are listed using the `list_db_tables` method.
    - The preprocessed DataFrame `date_data` is uploaded to the database with the table name 'dim_date_times' using the `upload_to_db_2` method of the `DatabaseConnector` class.

### Running the Script
To execute the script, ensure that all necessary dependencies are installed. Additionally, ensure that the required data files and database credentials are accessible.

```python
python date_data_upload.py
```

The script will retrieve data from the specified JSON file link, preprocess it, and upload it to the database. 

### Aicore Data Extraction Python Script

The Python script `extract_aicore_data.py` orchestrates the extraction, cleaning, and uploading of data from a PostgreSQL database to a MySQL database. Here's a breakdown of the code:

#### Importing Modules
- The script imports all necessary modules for data extraction, cleaning, and database interaction.

#### Main Function
1. **Extracting and Cleaning Data**:
    - An instance of `DatabaseConnector_postgres` is created to interact with the PostgreSQL database.
    - Existing tables in the PostgreSQL database are listed using the `list_db_tables` method.
    - Data is extracted from the specified table using the `read_rds_tables_postgress` method of the `DataExtractor` class. Only relevant columns are selected using `.iloc[:,1:]`.
    - Data cleaning is performed using the `clean_orders_data` method of the `DataCleaning` class to prepare the data for uploading.

2. **Uploading Data**:
    - An instance of `DatabaseConnector` is created to interact with the MySQL database.
    - Existing tables in the MySQL database are listed using the `list_db_tables` method.
    - The cleaned DataFrame `table_data` is uploaded to the MySQL database with the table name 'orders_table' using the `upload_to_db_2` method of the `DatabaseConnector` class.

### Running the Script
To execute the script, ensure that all necessary dependencies are installed. Additionally, ensure that the required database connections and credentials are properly configured and accessible.

```python
python extract_aicore_data.py
```

The script will extract data from the PostgreSQL database, clean it, and upload it to the MySQL database. 
