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
load_dotenv()
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
# DATA ASSETS
###############################################################################
exp_df, exp_status, exp_error = queries.query_get_current_experiments(client)
trial_df, trial_status, trial_error = queries.query_get_current_trials(client)
trial_params = queries.ExtractTrialData(client).fetch_data(client,
                                    "trial_parameters") 

###############################################################################
# APPLICATION
###############################################################################

st.markdown("---")
st.title("VALIDATION RUNS")
st.markdown("---")

# Instructions
st.subheader("Instructions")
st.caption("""On this page the user has the ability to execute a validation run.
This constitutes first electing a trial, and by extention its parameters.
Once executed the 
""")

# Experiment Table
st.subheader("Existing Experiments")
if not exp_status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(exp_df, use_container_width=True)

# Trials Table
st.subheader("Existing Trials")
if not trial_status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(trial_df, use_container_width=True)




# Select an Experiment

# Select Trial
trial_id = st.selectbox("Select Trial Id", trial_df['trial_id'].values.tolist())


# Trials Parameter Table

# Get Extractions
if trial_id:
    st.subheader("Trial Extractions")
    extractions = queries.ExtractTrialData(client=client).fetch_data(
        "trial_extractions", "dc7c-e32ce2ef"
    )
    extractions = extractions[extractions['trial_id'] == trial_id]

    st.dataframe(extractions, use_container_width=True)
        
        





