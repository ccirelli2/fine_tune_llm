"""
LlamaIndex + Ollama
- usage examples: https://docs.llamaindex.ai/en/stable/examples/llm/ollama/
- structured output: https://docs.llamaindex.ai/en/stable/module_guides/querying/structured_outputs/


Text to Speech
- https://www.geeksforgeeks.org/convert-text-speech-python/
"""

# Libraries
import os
import re
import argparse
import pandas as pd
import ollama
import mysql.connector
import chromadb
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from dotenv import load_dotenv
from datetime import datetime
from dotenv import load_dotenv
from fastembed import TextEmbedding
from transformers import LlamaTokenizer
from src import utils, rag, connections, queries

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

# Arguments
parser = argparse.ArgumentParser(description="simple parser")
parser.add_argument('--trial_id', type=str, required=True, help="Trial Id")
args = parser.parse_args()
trial_id = args.trial_id


###############################################################################
# Load Experiment Configurations
###############################################################################

print("\n\n")
print("======================================================================")
print("Loading Trial Data")
print("======================================================================")

# Instantiate Extractor
extractor = queries.ExtractTrialData(client=conn_mysql)

# Get Trial Data
trial_data = extractor.fetch_data(table_name="trials", trial_id=trial_id)

# Get Trial Parameters
trial_params = extractor.fetch_data(table_name="trial_parameters", trial_id=trial_id)

# Get Companies
company_df, co_status, co_error = queries.get_filing_index_companies(conn_mysql) 


###############################################################################
# Expose Trial Attributes
###############################################################################

print("\n\n")
print("======================================================================")
print("Extracting Trial Parameters")
print("======================================================================")

# Traial Name
trial_name = trial_params[trial_params['name'] == 'trial_name']['value'].values.tolist()
print(trial_name)
if isinstance(trial_name, list):
    trial_name = trial_name[0]

# Get Company CIK's
cik_param = trial_params[trial_params['name'] == 'cik']['value'].values.tolist()

# Get Financial Metrics
fin_metrics = trial_params[trial_params['name'] == 'financial-metric']['value'].values.tolist()

# Financial Metrics - Year
fin_year = trial_params[trial_params['name'] == 'financial-metric-year']['value'].values.tolist()

# Get Model String
model_str = trial_params[trial_params['name'] == 'model_str']['value'].values.tolist()[0]

print("Executing Trial {}-{}\n\n".format(trial_name, trial_id))
print("Trial Parameters\n\n{}".format(trial_params))
print("\n\n")


###############################################################################
# Data Transformations
###############################################################################

print("\n\n")
print("======================================================================")
print("Performing Data Transformations")
print("======================================================================")

# Normalize Financial Metric Name
fin_metrics = [utils.normalize_financial_metric_names(i) for i in fin_metrics]


###############################################################################
# Build Extraction Dataframe
###############################################################################

print("\n\n")
print("======================================================================")
print("Building Extraction Table")
print("======================================================================")
"Intersection of N companies by M financial Metrics"

params_to_explode = {
        'cik': cik_param,
        'financial_metric': fin_metrics,
        'financial_year': fin_year
}
extractions = pd.DataFrame({
    'trial_id': [trial_id],
})

for p in params_to_explode:
    extractions[p] = [params_to_explode[p] for i in range(extractions.shape[0])]
    extractions = extractions.explode(p)

# Add extraction id
extractions['call_id'] = [str(i) + '-' + trial_id
                          for i in range(extractions.shape[0])
]

# Join Company Metadata
extractions = pd.merge(extractions, company_df, on='cik', how='inner')


print("Extractions DataFrame is completed.")
print("Total expected extractions => {}".format(extractions.shape[0]))


###############################################################################
# Retreival
###############################################################################
# TODO: Replace iterative approach with async
print("\n\n")
print("======================================================================")
print("Starting Extractions")
print("======================================================================")


for i in extractions.iterrows():
    row = i[1]
    call_id = row.call_id.strip()
    trial_id = row.trial_id.strip()
    cik = row.cik.strip()
    company_name = row.company_name.strip()
    financial_metric = row.financial_metric.strip()
    financial_year = row.financial_year.strip()

    # Run Time Parameters
    conditions = {'year': financial_year}
    file_type = ["8-K", "10-Q", "10-K"]
    n_results = 10
    
    # Construct Query
    query = rag.query_single_attribute(
        name=financial_metric,
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
    # TODO FILING TYPE NEEDS TO BE ADDED TO STREAMLIT APP & TRIAL PARAMS
    # TODO Add N Results to Trial Params
    
    print("Obtaining data from collection")

    chroma_response = collection.query(
        query_embeddings=query_embedding,
        where={"$and": 
               [{"cik": cik},
                {"file_type": {"$in": file_type}},
            ]
        },
        n_results=n_results
    )
    print("Chunks Returned")
    context = chroma_response['documents'][0]
    print(f"Number of chunks returned => {len(context)}")


    ###########################################################################
    # Construct Prompts
    ###########################################################################

    # Construct Task
    print("Construct Task")
    date = datetime.today().strftime("%B %d, %Y")
    task = rag.task_single_attribute(
        name=financial_metric,
        conditions=conditions
    )
    print("\t Task => {}".format(task))

    # Construct Prompt
    print("Building prompt")
    # This is not correct.  Need to find a way to send separate chunks + ids.
    context = "\n".join(context)
    prompt = (
        rag
        .ConstructPromptWithRational(
            context=context,
            task=task,
        )
        .build()
    )
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
    print("Prompt => {}".format(prompt[:500]))


    ###############################################################################
    # Generation
    ###############################################################################

    # Model Configuration
    model_string = "llama3.1:latest" # TODO: replace with config model str.
    time_out = 120 # seconds
    json_mode = True   # add to trial config
    temperature = 0.0  # add to trial config
    start = datetime.now()

    # Instantiate Model
    try:

        llm = Ollama(
            model=model_string,
            request_timeout=time_out,
            json_mode=True,
            temperature=0.0
        )

        response_obj = llm.complete(prompt)
        print("Extraction successfull.  Response => {}".format(response))
    except Exception as e:
        print("Extraction failed with error => {}".format(e))
   
    import json
    response_json = response_obj.dict()['text']
    response_dict = json.loads(response_json)

    try:
        extracted_field_name = response_dict['field-name']
        extracted_value = response_dict['field-value']
        units = response_dict['units']
        chunk_used = response_dict['text']
        llm_logic = response_dict["explanation"]
        payload = json.dumps({"response_raw": response_json, "error": ""})
        print("Parsing json response successfull")

    except Exception as e:
        extracted_field_name = ""
        extracted_value = ""
        units = ""
        chunk_used = ""
        explanation = ""
        llm_logic = ""
        payload = json.dumps({"response_raw": response_json, "error": e})
        print("Parsing json response failed with error => {}".format(e))    
    
    duration = (datetime.now() - start).seconds

    
    # Insert results into trial extraction dataframe
    values = (
        call_id,
        trial_id,
        cik,
        company_name,
        str(financial_metric),
        str(financial_year),
        extracted_field_name,
        extracted_value,
        units,
        chunk_used,
        llm_logic,
        payload,
    )
    print("Extraction duration => {}".format(duration))
    print("Inserting Extraction Table")

    status, error = queries.insert_into_trial_extraction_table(conn_mysql, values)
    print("Error => {}".format(error))
