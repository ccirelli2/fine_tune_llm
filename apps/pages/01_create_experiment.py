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
st.title("EXPERIMENTS")
st.markdown("---")

# Current Experiments
st.header("Existing Experiments")
exp_df, status, error = queries.query_get_current_experiments(client)
if not status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(exp_df, use_container_width=True)

# Create Experiments
st.header("Create an Experiment")
exp_name = st.text_input("Enter name of experiment")
exp_desc = st.text_input("Enter description here")
exp_author = st.text_input("Enter your name here")
exp_created = datetime.now()

if st.button("Create Experiment"):
    st.write("Creating experiment")
    
    # Validate Uniqueness
    st.write("\tValidating uniqueness of experiment")
    exp_names_exist = exp_df['name'].values.tolist()
    if exp_name in exp_names_exist:
        msg = "Experiment name is not unique.  Please change"
        st.markdown(
            "<p style='color: red; font-weight: bold;'></p>".format(msg),
            unsafe_allow_html=True
        )
    else:
        st.write("\t\t Experiment name is unique")

        # Create Experiment id
        exp_id = str(uuid4())[:4]
        st.write("\tGenerating experiment id. => {}".format(exp_id))

        # Write to Experiment Database
        st.write("\tCreating Experiment")
        values = (exp_id, exp_name, exp_desc, exp_author, exp_created)
        response, error = queries.insert_into_experiments(client, values)
        if response:
            st.write("\t\tExperiment created successfully")
        else:
            msg = "Experiment creation failed with error => {}".format(error)
            st.markdown(
                "<p style='color: red; font-weight: bold;'>{}</p>".format(msg),
                unsafe_allow_html=True
            )









