"""

"""
# Libraries
import os
import mysql.connector
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import utils, queries, connections

# Directories                                                                      
DIR_ROOT = utils.get_root_directory()                                              
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')                              
DIR_TEXT_CLEAN = os.path.join(DIR_ROOT, 'data', 'text', 'clean')                    
                                                                                
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

# Query Data From Filing Index
query = "SELECT * FROM filing_index;"
filing_df = pd.read_sql(query, client)
client.close()

# Get All Files in Directory
files_local = os.listdir(DIR_TEXT_CLEAN)
files_db = filing_df['file_name'].values.tolist()
filing_diff = set(files_local).difference(files_db)
filing_common = set(files_local).intersection(files_db)
print("The following files are not localed in the database or local drive {}".
      format(filing_diff))

# Instantiate Splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=5_000,
    chunk_overlap=500,
    length_function=len,
)

# Iterate Filing DataFrame
for series in filing_df.iterrows():
    
    # Extract File Name (Foreign Key)
    row = series[1]
    file_name = row.file_name
    if file_name in filing_common:
    
        # Read Text
        path = os.path.join(DIR_TEXT_CLEAN, file_name)
        os.path.exists(path)

        with open(path, 'r') as f:
            text = f.read()




























