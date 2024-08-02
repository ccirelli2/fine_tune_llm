"""
"""
# Libraries                                                                        
import os                                                                          
import chromadb
import mysql.connector                                                             
import pandas as pd                                                                
from dotenv import load_dotenv
from fastembed import TextEmbedding
from src import utils, queries, connections                                        
                                                                                   
# Directories
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")
DIR_CONFIG = os.getenv("DIR_CONFIG")
DIR_DATA = os.getenv("DIR_DATA")
DIR_DATA_TEXT = os.getenv("DIR_DATA_TEXT")
DIR_TEXT_CLEAN = os.path.join(DIR_DATA_TEXT, 'clean') 

# Configurations
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config
CONFIG_CHROMA = utils.LoadConfig().load(file_name="chroma.yaml", directory=DIR_CONFIG).config

# MySql Connection Configurations
DATABASE = CONFIG_CONN['MYSQL']['DATABASE']                                     
HOST = CONFIG_CONN['MYSQL']['HOST']                                             
USER = CONFIG_CONN['MYSQL']['USER']                                             
PASSWORD = CONFIG_CONN['MYSQL']['PASSWORD']                                     
PORT = CONFIG_CONN['MYSQL']['PORT']                                             

# Chroma Configurations
COLLECTION_KEY = 'EDGAR'
COLLECTION_METADATA = CONFIG_CHROMA['COLLECTIONS']['EDGAR']['METADATA']
COLLECTION_NAME = COLLECTION_METADATA['name']
EMBED_MODEL = CONFIG_CHROMA['EMBEDDING_MODEL']

# Chroma Connection
# conn_chroma = chromadb.PersistentClient("/Users/temp-admin/chromadb")
conn_chroma = chromadb.HttpClient(host='localhost', port=8000)

# Establish Connection to MySql                                                 
conn_mysql = connections.MysqlClient().get_client(                                  
    host=HOST,                                                                  
    user=USER,                                                                  
    password=PASSWORD,                                                          
    port=PORT,                                                                  
    database=DATABASE                                                           
)                                                                               
cursor = conn_mysql.cursor() 

# Embedding Model
embedding_model = TextEmbedding(EMBED_MODEL)

###############################################################################
# Get Filing Index + Chunks
###############################################################################
'Note: for very large dataset we iteratively query mysql and insert into chroma'

query = queries.get_filing_index_join_chunks() 
chunk_df = pd.read_sql(query, conn_mysql)


###############################################################################
# Create Collection
###############################################################################

collection = conn_chroma.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata=COLLECTION_METADATA
)
print("Connection established to Chromadb collection => {}".format(
    COLLECTION_NAME)
)

# Create Upsert Vectors
record_cnt = chunk_df.shape[0]
print("Record Count => {}".format(record_cnt))

# Insert Rows Chromadb
upsert_cnt = 100
print("Upserting records {} at a time".format(upsert_cnt))

# Iterate Records
print("Begginging insertion")
for i in range(0, record_cnt, upsert_cnt):
    # Get Records
    start = i
    stop = i + upsert_cnt
    records = chunk_df.iloc[start: stop]
    print("\tUpserting records from {} to {} of {}".format(start, stop, record_cnt))

    # Create Fields to Upsert
    ids = records['chunk_id'].values.tolist()
    documents = records['chunk'].values.tolist()
    embeddings = [i.tolist() for i in list(embedding_model.embed(documents))]
    
    # Create Metadata Fields
    meta_fields = ["file_name", "file_type", "file_date", "company_name", "cik",
        "irs_number", "character_count", "token_count"]
    metadata_df = records[meta_fields]
    metadata = metadata_df.to_dict(orient='records')
    
    # Upsert
    collection.upsert(
        documents=documents,
        ids=ids,
        embeddings=embeddings,
        metadatas=metadata
    )
    
    print("\tInsertion completed.")

