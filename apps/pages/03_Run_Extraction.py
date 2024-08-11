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
trial_df = queries.ExtractTrialData(client).fetch_data("trials")
trial_params = queries.ExtractTrialData(client).fetch_data("trial_parameters") 
# TODO: Add get method for status code.

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
st.write("")
st.write("")

# Experiment Table
st.subheader("Existing Experiments")

if not exp_status:
    st.write("Query failed with error => {}".format(exp_error))
else:
    # Select An Experiment
    st.dataframe(exp_df, use_container_width=True)
    
    st.caption("Select An Experiment")
    exp_id = st.selectbox("Select Experiment ID", exp_df['id'].values.tolist())
    st.write("")
    st.write("")

    # Trials Table
    if exp_id:
        st.subheader("Existing Trials")
        trial_df = trial_df[trial_df['experiment_id'] == exp_id] 
        st.dataframe(trial_df, use_container_width=True)

        # Select Trial
        trial_id = st.selectbox("Select Trial Id", trial_df['trial_id'].values.tolist())
        st.write("")
        st.write("")

        # Trials Parameter Table
        if trial_id:
            st.subheader("Trial Parameters")
            trial_params = trial_params[trial_params['trial_id'] == trial_id]
            st.dataframe(trial_params, use_container_width=True)
            st.write("")
            st.write("")

            # Validate if Extraction Already Run
            extraction_exists = ""
            if extraction_exists:
                st.warning("Extraction already exists.  Please proceed to inspection")
            else:

                # Run Extraction
                st.subheader("Run Extraction")
                st.caption("Trial ID => {}".format(trial_id))
                if st.button("Execute"):
                    st.write("Executing Extraction Script for Trial => {}".format(trial_id))
                    flag = "--trial_id"                                                        
                    value = trial_id
                    path = "~/repositories/fine_tune_llm/transforms/extraction/run_extractions.py"
                    command = "poetry run python {} --trial_id {}".format(path, trial_id)   
                    os.system(command)
                    st.write("Script Finished")   



