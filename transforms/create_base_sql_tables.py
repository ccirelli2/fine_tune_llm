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

# Define Tables to Create
tables_2_create = {
    "filing_index": queries.command_create_mysql_filings_index_table(),
    "filing_chunks": queries.command_create_mysql_chunk_table(),
    "validation_num": queries.command_create_mysql_validation_num_table(),
    "validation_pre": queries.command_create_mysql_validation_pre_table(),
    "validation_sub": queries.command_create_mysql_validation_sub_table(),
    "validation_tag": queries.command_create_mysql_validation_tag_table()
}

# Create Tables
for table_name in tables_2_create:

    # Check if Table Exists
    table_exists = utils.check_table_exists(cursor, table_name, DATABASE)
    
    if not table_exists:
        print(f"\tCreating table => {table_name}")
        sql = tables_2_create[table_name]
        cursor.execute(sql)
        client.commit()
        print("\tSuccess\n")
