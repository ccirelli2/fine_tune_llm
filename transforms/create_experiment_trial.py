"""

"""
# Libraries
import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import utils, queries, connections

# Directories                                                                      
DIR_ROOT = os.getenv("DIR_ROOT")
DIR_CONFIG = os.getenv("DIR_CONFIG")
DIR_DATA = os.getenv("DIR_DATA")
DIR_TEXT_CLEAN = os.path.join(DIR_DATA, 'text', 'clean')                    
                                                                                
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


