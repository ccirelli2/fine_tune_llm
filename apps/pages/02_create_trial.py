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

client_alchemy = connections.MySqlAlchemyClient().get_client(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

###############################################################################
# DATA ARTIFACTS
###############################################################################

# MySql Experiments Table
exp_df, exp_status, exp_error = queries.query_get_current_experiments(client)

# MySql Trials Table
trial_df, trial_status, trial_error = queries.query_get_current_trials(client)

# MySql Models Table
models_df, models_status, models_error = queries.query_get_all_records_from_models(client)


###############################################################################
# APPLICATION
###############################################################################

st.markdown("---")
st.title("TRIAL BUILDER")
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
if not exp_status:
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
if not trial_status:
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
exp_name_elected = st.selectbox("Select Experiment Name", exp_names)

if exp_name_elected:
    st.write('Selected options:\t', exp_name_elected[0])

    # Get Experiment ID
    exp_id = exp_df[exp_df['name'] == exp_name_elected]['id'].values.tolist()[0]
    st.write("Experiment id => {}".format(exp_id))
    st.write("")
    st.write("")

    # Create Trial
    st.header("Trial Parameters")
    st.caption("Please visit each tab to construct the parameters for your trail")

    # Create Trial id
    trial_id = f"{exp_id}-{str(uuid4())[:8]}"

    # Instantiate Trial Parameter Accumulator
    accumulator = utils.TrialParamAccumulator(trial_id=trial_id)

    # Accumulate
    accumulator.log('experinment_id', exp_id, "experiment")
    accumulator.log('experiment_name', exp_name_elected, "experiment")

    # Create Tabs
    tabs = ['basic', 'model', 'companies', 'extraction']
    tab_basic, tab_models, tab_companies, tab_extract = st.tabs(tabs)
    
    with tab_basic:
        trial_name = st.text_input("Enter name of trial")
        trial_desc = st.text_input("Enter description here")
        trial_outcome = st.text_input("Enter outcome expected from trial")
        trial_author = st.text_input("Enter your name here")
        trial_created = datetime.now()
        accumulator.log('trial_name', trial_name, "trial")
        accumulator.log('trial_desc', trial_desc, "trial")
        accumulator.log('trial_outcome', trial_outcome, "trial")
        accumulator.log('trial_author', trial_author, "trial")
        accumulator.log('trial_created', trial_created, "trial")

        if not all([trial_name, trial_desc, trial_outcome, trial_author,
                    trial_created]
            ):
            st.warning("WARNING: All basic information must be filled in")

    with tab_models:
        if not exp_status:
            st.write("Load table failed with error => {}".format(error))
        else:
            st.markdown(
                "<small>Query successfull.</small>",
                unsafe_allow_html=True
            )
            st.dataframe(models_df, use_container_width=True)
        
        models = models_df['model_str'].values.tolist()
        model_election = st.selectbox("Select model", models)
        accumulator.log("model_str", model_election, "model")

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
                    company_cik = companies_df['cik'].values.tolist()
                    company_elections = companies_df['company_name'].values.tolist()
                    
                    for i in range(len(company_elections)):
                        cik = company_cik[i]
                        company_name = company_elections[i]
                        # TODO: add another generic field to capture things like company name
                        accumulator.log("cik", cik, "companies")
                    
                    st.write("Company count => {}".format(len(company_elections)))

            with tab_individual:
                company_elections = st.multiselect('Select options:', company_list)
                if len(company_elections) == 0:
                    st.warning("You must select at least one company")
            
                if company_elections:
                    st.write(f"Adding {len(company_elections)} companies")
                 
                    company_cik = (
                        companies_df[
                            companies_df['company_name'].isin(company_elections)
                            ]['cik']
                        .values
                        .tolist()
                    )
                    for i in range(len(company_elections)):
                        cik = company_cik[i]
                        company_name = company_elections[i]
                        accumulator.log("cik", cik, "companies")

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
        
        for f in financial_elections:
            accumulator.log("financial-metric", f, "financial_metrics")

    st.write("")
    st.write("")

###############################################################################
# Create Trial
###############################################################################
    st.header("Proceed to Create Trial")


    tab_create, tab_accounting = st.tabs(['create trial', 'inspect selections'])

    with tab_accounting:
        st.write("")
        st.write("")
        accumulator_df = accumulator.get_dataframe()
        st.dataframe(accumulator_df, width=1_000)

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
                st.write("\tGenerating trial id => {}".format(trial_id))

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


                # Write to Trial Parameters table
                st.write("Writing trial parameters to trial_parameters mysql table")
                status, error = queries.insert_into_trial_parameters_table(
                    client=client_alchemy,
                    df=accumulator_df
                )
                if not status:
                    st.write("Insertion failed with error => {}".format(error))
                else:
                    st.write("Writing successfull")

                


