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

# Current Experiments
st.subheader("Existing Experiments")
exp_df, status, error = queries.query_get_current_experiments(client)
if not status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(exp_df, use_container_width=True)

# Current Trials
st.subheader("Existing Trials")
trial_df, status, error = queries.query_get_current_trials(client)
if not status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(trial_df, use_container_width=True)

# Select an Experiment
st.subheader("Select An Experiment")
exp_names = exp_df['name'].values.tolist()
checkbox_states = {item: st.checkbox(item) for item in exp_names}
exp_name_elected = [item for item, is_checked in checkbox_states.items() if is_checked]


        
        





