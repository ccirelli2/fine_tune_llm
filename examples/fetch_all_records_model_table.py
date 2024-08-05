"""
Example of how to create a sql table
"""
import os
from dotenv import load_dotenv
from src import queries, utils, connections

# Directories
DIR_ROOT = utils.get_root_directory()
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')

# Load Configuration Files
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config

# Connection Configurations
load_dotenv()
HOST = CONFIG_CONN['MYSQL']['HOST']
USER = CONFIG_CONN['MYSQL']['USER']
PASSWORD = os.getenv("MYSQL_PASSWORD")
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



models_df = queries.fetch_all_records_from_models(client)

print(models_df.head())

