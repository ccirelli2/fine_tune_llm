"""
Dependencies
    Connection to MySql
    Connection to ChromadB
    Prompt Template(s)
    Query Template(s)
    Ollama
    Query Experiment & Trial parameters from mysql tables.
    Write extraction to mysql.

"""

# Libraries
import os
import pandas as pd
import ollama
import mysql.connector
import chromadb
from fastembed import TextEmbedding

# Directories
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               
DIR_DATA = os.getenv("DIR_DATA_TEXT")                                              
DIR_TEXT_RAW = os.path.join(DIR_DATA_TEXT, 'raw')
DIR_TEXT_CLEAN = os.path.join(DIR_DATA_TEXT, 'clean')  

# Config Files
CONFIG_MYSQL = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config
CONFIG_CHROMA = utils.LoadConfig().load(file_name="chroma.yaml", directory=DIR_CONFIG).config

# MySQL - Connection
HOST = CONFIG_MYSQL['MYSQL']['HOST']                                             
USER = CONFIG_MYSQL['MYSQL']['USER']                                             
PASSWORD = CONFIG_MYSQL['MYSQL']['PASSWORD']                                     
PORT = CONFIG_MYSQL['MYSQL']['PORT']                                             
DATABASE = CONFIG_MYSQL['MYSQL']['DATABASE']                                     
                                                                                
conn_mysql = connections.MysqlClient().get_client(                                  
    host=HOST,                                                                  
    user=USER,                                                                  
    password=PASSWORD,                                                          
    port=PORT,                                                                  
    database=DATABASE                                                           
)                                                                                                 
cursor_mysql = conn_mysql.cursor()

# ChromaDb - Connection
COLLECTION_KEY = "EDGAR"
COLLECTION_METADATA = CONFIG_CHROMA['COLLECTIONS']['COLLECTION_KEY']['METADATA']
COLLECTION_NAME = COLLECTION_METADATA['name']
EMBED_MODEL = CONFIG_CHROMA['EMBEDDING_MODEL']

conn_chroma = chromadb.HttpClient(
        host='localhost', port=8000
)

# Embedding Model
embedding_model = TextEmbedding(EMBED_MODEL) 

# Load Query Template Functions

# Load Prompt Template Functions


###############################################################################
# Parameters
###############################################################################

# Get Company Names


# Get Financial Metrics


# Iterate Company Name (CIK) + Financial Metric

###############################################################################
# Retreival
###############################################################################

# Construct Queries


# Retrieve Chunks / Text



###############################################################################
# Extraction
###############################################################################

# Construct Prompts


# Execute Extraction



###############################################################################
# Write Results to MySql Trial Results Table
###############################################################################




