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
)

# Get Cursor
cursor = client.cursor()

# Define Databases to Create
db_2_create = {
    "edgar_database": queries.create_edgar_database(),
}

# Create Databases
for db_name in db_2_create:
    print("Checking if database {} exists".format(db_name))

    if not utils.check_database_exists(cursor, "edgar"):
        print("Creating database")
        sql = db_2_create[db_name]
        cursor.execute(sql)
        client.commit()
        print("Completed")
    else:
        print("Database exists")
