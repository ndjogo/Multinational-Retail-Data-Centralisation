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

Ensure that the `db_creds.yaml` file containing AWS credentials is available in the same directory as the script.