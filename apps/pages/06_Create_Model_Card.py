import os
import streamlit as st
import pandas as pd
from datetime import datetime
from uuid import uuid4
from dotenv import load_dotenv
from src import queries, utils, connections

# Directories                                                                   
load_dotenv()                                                                   
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               
                                                                                
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

###############################################################################
# APPLICATION
###############################################################################

st.markdown("---")
st.title("CREATE MODEL CARD")
st.markdown("---")

# Current Experiments
st.header("Existing Models")
model_df, status, error = queries.query_get_all_records_from_models(client)

if not status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(model_df, use_container_width=True)
    st.markdown(
            "<small>Number of Records {}</small>".format(model_df.shape[0]),
            unsafe_allow_html=True
    )



# Create Experiments
st.header("Add a New Model")
model_name = st.text_input("Enter model name")
model_checkpoint = st.text_input("Enter model checkpoint")
model_version = st.text_input("Enter model version")
model_desc = st.text_input("Enter model description")
model_source = st.text_input("Enter model source")
model_created = datetime.now()


if st.button("Add Model"):
    st.write("Adding model")
    
    # Create Model ID
    model_id = str(uuid4())[:4]
    st.write("\tGenerating model id. => {}".format(model_id))

    # Write to Model Table
    st.write("\tInserting Model Data")
    values = (model_id, model_name, model_checkpoint, model_version, model_desc, model_source, model_created)
    response, error = queries.insert_into_models_table(client, values)
    if response:
        st.write("\t\tModel Created Successfully")
    else:
        msg = "Model card creation failed with error => {}".format(error)
        st.markdown(
            "<p style='color: red; font-weight: bold;'>{}</p>".format(msg),
            unsafe_allow_html=True
        )







