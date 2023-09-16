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

That's it! You should now have MySQL installed and running on your system. You can access it using the MySQL command-line client or other MySQL management tools like MySQL Workbench.
Usage instructions
File structure of the project
License information
