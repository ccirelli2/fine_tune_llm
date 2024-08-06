"""
LlamaIndex + Ollama
- https://docs.llamaindex.ai/en/stable/examples/llm/ollama/
"""

# Libraries
import os
import pandas as pd
import ollama
import mysql.connector
import chromadb
from dotenv import load_dotenv
from datetime import datetime
from dotenv import load_dotenv
from fastembed import TextEmbedding
from transformers import LlamaTokenizer
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
PASSWORD = os.getenv('MYSQL_PASSWORD')                                     
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
# LOAD TRIAL CONFIGURATION
###############################################################################

trial_id = "1234"  # replace with argparse variable so that we can call this
                   # script from streamlit application.

# Trial Table

# Trial Parameters Table

# Expose Attributes

###############################################################################
# Temporary Configurations (Will Switch to MySql Trials Table)
###############################################################################

# Get Company Names


# Get Financial Metrics
fields = {
    0: {
        "name_source": "NetIncomeLoss",
        "name_normalized": "Net Income Loss",
        "conditions": {"year": 2021}
    },

    1: {
        "name_source": "EarningsPerShareDiluted",
        "name_normalized": "Earnings Per Share Diluted",
        "conditions": {"year": 2021}
    }
}
company_name = {
        0: {"name": "ServiceNow, Inc.", "cik": "0001373715"},
        1: {"name": "EDISON INTERNATIONAL", "cik": "0000827052"}
}


###############################################################################
# Retreival
###############################################################################

# Construct Query
query = rag.query_single_attribute(
    name=fields[0]["name_normalized"],
    conditions=fields[0]['conditions']
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
print("Obtaining data from collection")
file_type = ["8-K", "10-Q", "10-K"]
chroma_response = collection.query(
    query_embeddings=query_embedding,
    where={"$and": 
           [{"cik": "0001373715"},
            {"file_type": {"$in": ["8-K"]}},
        ]
    },
    n_results=10
)
print("Chunks Returned")
context = chroma_response['documents'][0]
print(f"Number of chunks returned => {len(context)}")


###############################################################################
# Construct Prompts
###############################################################################


# Construct Task
print("Construct Task")
date = datetime.today().strftime("%B %d, %Y")
task = rag.task_single_attribute(
    name=fields[0]['name_normalized'],
    conditions=fields[0]['conditions']
)
print("\t Task => {}".format(task))

# Construct Prompt
print("Building prompt")
context = "\n".join(context)
example = {"key": "value"}
prompt = rag.ConstructPromptWithRational(context=context, task=task, example=example).build()
print("Prompt completed")

# Execute Extraction
role = "user"
messages = [{'role': role, 'content': prompt}]                                  
print("Generation")
start = datetime.now()
response = ollama.generate(                                                     
    model='llama3.1:latest',
    prompt=prompt,                                                          
)                                                                               
"""
model = response['model']
extraction_response = response['response']                                                  
extraction_context = response['context']
tokenizer = LlamaTokenizer.from_pretrained("llama3.1")
extraction_context_decoded = tokenizer 

print("LLM Response => {}".format(content))
print("LLM Raw Response => \n\n {}".format(response))
"""
print("LLM Reponse => {}".format(response))
duration = datetime.now() - start
print("Duration => {}".format(duration))


###############################################################################
# Write Results to MySql Trial Results Table
###############################################################################




