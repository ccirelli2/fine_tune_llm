"""
TODO: Switch to using langchain for rag orchestration
TODO: Our validation results table will need to have both the raw & normalized
    names for the financial metrics.

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
from dotenv import load_dotenv
from fastembed import TextEmbedding
from src import utils, rag, connections

# Directories
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               

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
COLLECTION_METADATA = CONFIG_CHROMA['COLLECTIONS'][COLLECTION_KEY]['METADATA']
COLLECTION_NAME = COLLECTION_METADATA['name']
EMBED_MODEL = CONFIG_CHROMA['EMBEDDING_MODEL']

conn_chroma = chromadb.HttpClient(
        host='localhost', port=8000
)

# Embedding Model
embedding_model = TextEmbedding(EMBED_MODEL) 


###############################################################################
# Temporary Configurations (Will Switch to MySql Trials Table)
###############################################################################

# Get Company Names


# Get Financial Metrics
fields = {
    0: {"name_val": "NetIncomeLoss", "name_norm": "Net Income Loss"},
    1: {}
}
conditions = {"year": 2021}
company_name = "3D SYSTEMS CORP"

company_cik = ""


###############################################################################
# Retreival
###############################################################################

# Construct Queries
query = rag.query_single_attribute(
    name=fields[0]["name_norm"],
    conditions=conditions
)
print("Query => {}".format(query))

# Get Collection
print("Obtaining collection => {}".format(COLLECTION_NAME))
collection = conn_chroma.get_or_create_collection(name=COLLECTION_NAME)

# Embed Query
print("Embedding query")
query_embedding = list(embedding_model.embed(query))[0].tolist()

# Retrieving Chunks
"""
NOTE: WE NEED TO ADD METADATA: EX CIK + YEAR
"""

context = collection.query(
    query_embeddings=query_embedding,
    n_results=5
)

print(context)


###############################################################################
# Extraction
###############################################################################

# Construct Prompts


# Execute Extraction
"""
messages = [{'role': role, 'content': prompt}]                                  
                                                                                
response = ollama.generate(                                                     
        model='llama3.1',                                                       
        prompt=prompt,                                                          
)                                                                               
content = response['response']                                                  
                                                                                
print(content)    
"""

###############################################################################
# Write Results to MySql Trial Results Table
###############################################################################




