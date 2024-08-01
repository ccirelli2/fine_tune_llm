"""
"""
import os
import re
import pandas as pd
from src import queries, utils, connections, transforms

# Directories
DIR_ROOT = utils.get_root_directory()
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')
DIR_TEXT_RAW = os.path.join(DIR_ROOT, 'data', 'text', 'raw')

# Load Configuration Files                                                      
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config

# Get List of Files
files = os.listdir(DIR_TEXT_RAW)
                                                                                
# Connection Configurations                                                     
HOST = CONFIG_CONN['MYSQL']['HOST']                                             
USER = CONFIG_CONN['MYSQL']['USER']                                             
PASSWORD = CONFIG_CONN['MYSQL']['PASSWORD']                                     
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

# Load Files
patterns = {
        "CIK": "CENTRAL INDEX KEY:.*\n",
        "FILING_TYPE": "CONFORMED SUBMISSION TYPE:.*\n",
        "FILING_DATE": "FILED AS OF DATE:.*\n",
        "COMPANY_NAME": "COMPANY CONFORMED NAME:.*\n",
        "CIK": "CENTRAL INDEX KEY:.*\n",
        "IRS_NUMBER": "IRS NUMBER:.*\n",
}

# Create Index Table From Filings
indexer = transforms.FilingIndex(
    directory=DIR_TEXT_RAW,
    patterns=patterns
    )

filings_df = indexer.transform()

# Insert Rows into MySql DataFrame
table_name = "filing_index"
for i in filings_df.iterrows():
    
    row = i[1]
    id_ = row.ID
    file_name = row.FILE_NAME
    file_type = row.FILING_TYPE
    filing_date = row.FILING_DATE
    company_name = row.COMPANY_NAME
    cik = row.CIK
    irs_number = row.IRS_NUMBER
    
    # Create Value Object
    values = (id_, file_name, file_type, filing_date, company_name, cik, irs_number)
    
    # Make Insertion
    queries.insert_into_filing_index_table(client, values)



