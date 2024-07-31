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
    name=COLLECTION_NAME
)

# Query
query = 'financials'
query_embedding = list(embedding_model.embed(query))[0].tolist()

results = collection.query(
    query_texts=[query],
    #query_embeddings=query_embedding,
    n_results=2
)

print(results)





