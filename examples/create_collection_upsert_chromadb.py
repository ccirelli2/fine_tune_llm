"""
"""
# Libraries                                                                        
import os                                                                          
import chromadb
import mysql.connector                                                             
import pandas as pd                                                                
from fastembed import TextEmbedding
from src import utils, queries, connections                                        
                                                                                   
# Directories                                                                      
DIR_ROOT = utils.get_root_directory()                                              
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')                              
DIR_TEXT_CLEAN = os.path.join(DIR_ROOT, 'data', 'text', 'clean') 

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
COLLECTION_KEY = 'SMOTE_TEST'
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
# Create Collection
###############################################################################

collection = conn_chroma.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata=COLLECTION_METADATA
)

# Records
text = "Ford Motor company sells cars"
embeddings = list(embedding_model.embed(text))[0].tolist()
ids = ["adfadsf"]
metadata = [{'date': '08-01-2024'}]

print(f"Upserting => {text}\n{ids}\n{metadata}")
collection.upsert(
    documents=[text],
    ids=ids,
    embeddings=embeddings,
    metadatas=metadata
)

print("Querying Database")
response = collection.query(query_texts=['Ford'], n_results=1)
print(response)






