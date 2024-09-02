"""
TODO: We need to write an asynchronous function or class to process and upsert
    these files

TODO: Why would it be the case that we have ~800 files in the local drive
but not in the mysql filing_index table?
"""
# Libraries
import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import utils, queries, connections

# Directories
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")
DIR_CONFIG = os.getenv("DIR_CONFIG")
DIR_DATA = os.getenv("DIR_DATA")
DIR_TEXT_CLEAN = os.path.join(DIR_DATA, 'text', 'clean')                    
                                                                                
# Load Configuration Files                                                      
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config
                                                                                
# Connection Configurations                                                     
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

# Get Cursor
cursor = client.cursor()

# Query Data From Filing Index
query = "SELECT * FROM filing_index;"
filing_df = pd.read_sql(query, client)

# Get All Files in Directory
files_local = os.listdir(DIR_TEXT_CLEAN)
files_db = filing_df['file_name'].values.tolist()
filing_diff = set(files_local).difference(files_db)
filing_common = set(files_local).intersection(files_db)

print("Total filings found => {}".format(len(filing_common)))
print("Total filings not in database => {}".format(len(filing_diff)))


# Instantiate Splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=5_000,
    chunk_overlap=500,
    length_function=len,
)

# SQL Statement
sql = """
    INSERT INTO filing_chunks
        (id, chunk, character_count, token_count, foreign_id)
        VALUES
        (%s, %s, %s, %s, %s);
    """

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

        # Chunk Text
        chunks = list(splitter.split_text(text))

        # Insert Chunks into filing_chunk table
        count = 0
        for c in chunks:
            
            # Create Insertion Values
            id_ = "{}-{}".format(file_name, count)
            count += 1
            char_cnt = len(c)
            token_cnt = len(c.split(" "))
            foreign_id = file_name
            values = (id_, c, char_cnt, token_cnt, foreign_id)
            
            # Insert
            try:
                print("Inserting Values for {}-{}".format(id_, foreign_id))
                cursor.execute(sql, values)
                client.commit()
                print("Successfull")
            except Exception as e:
                print("Insertion failed with exception => {}".format(e))
