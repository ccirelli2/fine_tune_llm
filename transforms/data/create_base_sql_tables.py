"""
Transform to create sql table 
"""
import os
from dotenv import load_dotenv
from mysql.connector.cursor_cext import CMySQLCursor
from src import queries, utils, connections

# Directories
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               

# Load Configuration Files
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config

# Connection Configurations
load_dotenv()
HOST = CONFIG_CONN['MYSQL']['HOST']
USER = CONFIG_CONN['MYSQL']['USER']
PASSWORD = os.getenv('MYSQL_PASSWORD')
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
    "rag_queries": queries.command_create_mysql_rag_queries_table(),
    "rag_prompt": queries.command_create_mysql_rag_prompt_table(),
    "filing_chunks": queries.command_create_mysql_chunk_table(),
    "validation_num": queries.command_create_mysql_validation_num_table(),
    "validation_pre": queries.command_create_mysql_validation_pre_table(),
    "validation_sub": queries.command_create_mysql_validation_sub_table(),
    "validation_tag": queries.command_create_mysql_validation_tag_table(),
    "experiments": queries.command_create_mysql_experiments_table(),
    "trials": queries.command_create_mysql_trials_table(),
    "trial_parameters": queries.command_create_mysql_trial_parameters_table(),
    "trial_extraction": queries.command_create_mysql_trial_extraction_table(),
    "trial_results": queries.command_create_mysql_trial_results_table(),
    "models": queries.command_create_mysql_models_table()
}


for table_name in tables_2_create:

    # Check if Table Exists
    table_exists = utils.check_table_exists(cursor, table_name, DATABASE)
    
    if not table_exists:
        try:
            print(f"\tCreating table => {table_name}")
            sql = tables_2_create[table_name]
            cursor.execute(sql)
            client.commit()
            print("\tSuccess\n")
        except Exception as e:
            print(e)
