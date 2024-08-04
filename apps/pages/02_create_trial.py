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

# Accumulator for Elections
accumulator = {}

###############################################################################
# APPLICATION
###############################################################################

st.markdown("---")
st.title("TRIALS")
st.markdown("---")

# Instructions
st.header("Instructions")
st.caption("""Trials are iterations of an experiment.  They are intended to test
some additional parameter value or environment setup.  Below you will be asked
to first elect an experiment for which to create a trial.  In the future you
will be presented with additional options and or parameters for a trial.
""")
st.write("")
st.write("")

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
st.write("")
st.write("")

# Current Trials
st.header("Existing Trials")
trial_df, status, error = queries.query_get_current_trials(client)
if not status:
    st.write("Query failed with error => {}".format(error))
else:
    st.markdown(
        "<small>Query successfull.</small>",
        unsafe_allow_html=True
    )
    st.dataframe(trial_df, use_container_width=True)
st.write("")
st.write("")

# Select an Experiment
st.header("Select An Experiment")
exp_names = exp_df['name'].values.tolist()
checkbox_states = {item: st.checkbox(item) for item in exp_names}
exp_name_elected = [item for item, is_checked in checkbox_states.items() if is_checked]
accumulator['experiment_name'] = exp_name_elected

if exp_name_elected:
    st.write('Selected options:\t', exp_name_elected[0])

    # Get Experiment ID
    exp_id = exp_df[exp_df['name'] == exp_name_elected]['id'].values.tolist()[0]
    accumulator['experinment_id'] = exp_id
    st.write("Experiment id => {}".format(exp_id))
    st.write("")
    st.write("")

    # Create Trial
    st.header("Trial Elections")

    # Create Tabs
    tabs = ['basic', 'model', 'companies', 'extraction']
    tab_basic, tab_models, tab_companies, tab_extract = st.tabs(tabs)
    
    with tab_basic:
        trial_name = st.text_input("Enter name of trial")
        trial_desc = st.text_input("Enter description here")
        trial_outcome = st.text_input("Enter outcome expected from trial")
        trial_author = st.text_input("Enter your name here")
        trial_created = datetime.now()
        accumulator['trial_name'] = trial_name
        accumulator['trial_desc'] = trial_desc
        accumulator['trial_outcome'] = trial_outcome
        accumulator['trial_author'] = trial_author
        accumulator['trial_created'] = trial_created

        if not all([trial_name, trial_desc, trial_outcome, trial_author,
                    trial_created]
            ):
            st.warning("WARNING: All basic information must be filled in")

    with tab_models:
        st.caption("TODO: Add query to models table")
        model_election = st.multiselect("Select model", ["llama3", "llama3.1"])
        accumulator['model'] = model_election

    with tab_companies:
        st.subheader("Companies From Filing Index")
        companies_df, status, error = queries.get_filing_index_companies(client)
        if not status:
            st.warning(f"WARNING: Query Failed with error => {error}")
        else:
            st.dataframe(companies_df)
            company_list = companies_df['company_name'].values.tolist()

            # Make Selections
            st.subheader("Company Selection")
            
            # Tabs
            tabs = ['all', 'individual']
            tab_all, tab_individual = st.tabs(tabs)
            with tab_all:
                if st.button("Confirm selection"):
                    company_elections = companies_df['cik'].values.tolist()
                    accumulator['companies'] = company_elections
                    st.write("Company count => {}".format(len(company_elections)))

            with tab_individual: 
                selected_options = st.multiselect('Select options:', company_list)
                
                if st.button("Confirm Selection"):
                    st.write(f"Company Count => {len(selected_options)}")
                    
                    companies_elections = (
                        companies_df[
                            companies_df['company_name'].isin(selected_options)
                            ]['cik']
                        .values
                        .tolist()
                    )
                    accumulator['companies'] = company_elections

    with tab_extract:
        st.caption("Select which financial metrics to extract")
        # TODO: Switch hard coded values for dynamically sourced from val dataset.
        options = [
                "StockholdersEquity",
                "NetIncomeLoss",
                "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
                "OperatingIncomeLoss",
                "EarningsPerShareBasic",
                "WeightedAverageNumberOfSharesOutstandingBasic",
                "IncomeTaxExpenseBenefit",
                "EarningsPerShareDiluted",
                "Assets",
                "NetCashProvidedByUsedInOperatingActivities"
        ]
        financial_elections = st.multiselect("Financial Variables", options)
        accumulator['financial_metrics'] = financial_elections

st.write("")
st.write("")

###############################################################################
# Create Trial
###############################################################################
st.header("Proceed to Create Trial")


tab_create, tab_accounting = st.tabs(['create trial', 'selection accounting'])

with tab_accounting:
    st.write("")
    st.write("")

    st.write(accumulator)

with tab_create:
    st.write("")
    st.write("")

    if st.button("Create Trial"):
            
        # Validate Uniqueness
        st.write("\tValidating uniqueness of trial name")
        trial_names_exist = trial_df['name'].values.tolist()

        if trial_name in trial_names_exist:
            msg = "Trial name is not unique.  Please change"
            st.markdown(
                "<p style='color: red; font-weight: bold;'></p>".format(msg),
                unsafe_allow_html=True
            )
        else:
            st.write("\t\t Trial name is unique")
            
            # Create Trial id
            trial_id = f"{exp_id}-{str(uuid4())[:8]}"
            st.write("\tGenerating trial id => {}".format(trial_id))

            # Other Elections
            tabs = ['model', 'validation-type']
            st.tabs(tabs)


            # Write to Trial
            st.write("\tCreating Trial")

            values = (
                trial_id, trial_name, trial_desc, trial_outcome, trial_author,
                exp_id, trial_created
            )
            response, error = queries.insert_into_trials(client, values)
            
            if not response:
                msg = "Trial creation failed with error => {}".format(error)
                st.markdown(
                    "<p style='color: red; font-weight: bold;'>{}</p>".format(msg),
                    unsafe_allow_html=True
                )
            else:
                st.write("\t\tTrial created successfully")



