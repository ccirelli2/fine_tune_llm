"""
TODO: We need to write an asynchronous function or class to process and upsert
    these files

TODO: Why would it be the case that we have ~800 files in the local drive
but not in the mysql filing_index table?
"""
# Libraries
import os
import asyncio
import aiofiles
import aiomysql
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
ASYNCH_IO_CONFIG_CONN = {key.lower(): value for key, value in CONFIG_CONN['MYSQL'].items()}
del ASYNCH_IO_CONFIG_CONN['database']
ASYNCH_IO_CONFIG_CONN['db'] = DATABASE
ASYNCH_IO_CONFIG_CONN['password'] = PASSWORD

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

# Instantiate Splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=5_000,
    chunk_overlap=500,
    length_function=len,
)

async def get_db_connection():
    return await aiomysql.connect(**ASYNCH_IO_CONFIG_CONN)

async def process_file(file_name, connection):
    path = os.path.join(DIR_TEXT_CLEAN, file_name)

    # TODO: Need to add auto rec coding.
    async with aiofiles.open(path, 'r') as f:
        text = await f.read()

    # Chunk Text
    chunks = list(splitter.split_text(text))

    async with connection.cursor() as cursor:
        sql = """
            INSERT INTO filing_chunks
                (id, chunk, character_count, token_count, foreign_id)
                VALUES
                (%s, %s, %s, %s, %s);
        """
        count = 0
        for c in chunks:
            id_ = "{}-{}".format(file_name, count)
            count += 1
            char_cnt = len(c)
            token_cnt = len(c.split(" "))
            foreign_id = file_name
            values = (id_, c, char_cnt, token_cnt, foreign_id)

            try:
                await cursor.execute(sql, values)
                await connection.commit()
                print(f"Inserting Values for {id_}-{foreign_id} - Success")
            except Exception as e:
                print(f"Insertion failed with exception => {e}")

async def main():
    # Get DB Connection
    connection = await get_db_connection()

    try:
        # Query Data From Filing Index
        query = "SELECT * FROM filing_index;"
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()

        # Create DataFrame from query results
        filing_df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

        # Get All Files in Directory
        files_local = os.listdir(DIR_TEXT_CLEAN)
        files_db = filing_df['file_name'].tolist()
        filing_diff = set(files_local).difference(files_db)
        filing_common = set(files_local).intersection(files_db)

        print(f"Total filings found => {len(filing_common)}")
        print(f"Total filings not in database => {len(filing_diff)}")

        # Limit the number of concurrent tasks
        semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent tasks

        async def sem_task(file_name):
            async with semaphore:
                await process_file(file_name, connection)

        # Process Files
        tasks = [sem_task(file_name) for file_name in filing_common]
        await asyncio.gather(*tasks)

    finally:
        connection.close()

# Run the main function
asyncio.run(main())
