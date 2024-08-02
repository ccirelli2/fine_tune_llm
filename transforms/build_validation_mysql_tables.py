"""
Script to insert validation data into base validation mysql tables.

column-config: coincides with sql table schema.
data: actual csv files downloaded from edgar
commands: unique table sql insert commands
"""
# Libraries
import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import utils, queries, connections

# Directories                 
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               
DIR_DATA = os.getenv("DIR_DATA")
DIR_DATA = os.path.join(DIR_ROOT, 'data', 'validation', 'clean')

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

# Columns
column_config = {
    "num": ["adsh", "tag", "version", "coreg", "ddate", "qtrs", "uom", "value", "footnote"],
    "pre": ["adsh", "report", "line", "stmt", "inpth", "rfile", "tag", "version",
        "plabel", "negating"],
    "sub": ["adsh","cik","name","sic","countryba","stprba","cityba","zipba",
        "bas1","bas2", "baph", "countryma","stprma", "cityma","zipma","mas1",
        "mas2","countryinc", "stprinc","ein","former","changed","afs","wksi",
        "fye","fye","form","period", "fy","fp","filed","accepted","prevrpt",
        "detail","instance","nciks","aciks"],
    "tag": ["tag", "version", "custom", "abstract", "datatype", "iord", "crdr",
            "tlabel", "doc"],
}

# Load Data
print("Loading DataFrames")
data_config = {
    "num": pd.read_csv(os.path.join(DIR_DATA, 'num.csv'), usecols=column_config['num']),
    "pre": pd.read_csv(os.path.join(DIR_DATA, 'pre.csv'), usecols=column_config['pre']),
    "sub": pd.read_csv(os.path.join(DIR_DATA, 'sub.csv'), usecols=column_config['sub']),
    "tag": pd.read_csv(os.path.join(DIR_DATA, 'tag.csv'), usecols=column_config['tag']),
}
print("Loading Completed")

# Command Config
command_config = {
    "num": queries.insert_into_validation_num,
    "pre": queries.insert_into_validation_pre,
    "sub": queries.insert_into_validation_sub,
    "tag": queries.insert_into_validation_tag,
}

# Make Insertions
table_names = [
    "num",
    "pre",
    "sub",
    "tag"
]

for table in table_names:
    # Load Data
    print(f"Loading data for table => {table}")
    data = data_config[table]
    # Build Values Object
    for series in data.iterrows():
        row = series[1]
        values = [str(row.to_dict()[key]) for key in column_config[table]]
        # Make Insertions
        command_config[table](client, values)

