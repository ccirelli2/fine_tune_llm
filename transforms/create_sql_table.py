"""
Transform to create sql table 
"""
import os
from mysql.connector.cursor_cext import CMySQLCursor
from src import queries, utils, connections

# Directories
DIR_ROOT = utils.get_root_directory()
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')

# Load Configuration Files
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config

# Connection Configurations
HOST = CONFIG_CONN['MYSQL']['HOST']
USER = CONFIG_CONN['MYSQL']['USER']
PASSWORD = CONFIG_CONN['MYSQL']['PASSWORD']
PORT = CONFIG_CONN['MYSQL']['PORT']
DATABASE = CONFIG_CONN['MYSQL']['DATABASE']

# Establish Connection to MySql
client = connections.MysqlClient().get_client(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
    database=DATABASE
)


# Get Cursor
cursor = client.cursor()

# Check if table already exists
table_exists = utils.check_table_exists(cursor, "filing_index", DATABASE)


print(cursor)

# Create Table
if not table_exists:
    try:
        client = connections.MysqlClient().get_client(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT,
            database=DATABASE
        )
        cursor = client.cursor()
        cursor.execute(queries.create_mysql_filings_index_table)
        cursor.close()
        print("table created successfully")
    except Exception as e:
        print("Create table returned an error => {}".format(e))


