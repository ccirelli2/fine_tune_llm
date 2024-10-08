"""
"""
import os
import re
import pandas as pd
from dotenv import load_dotenv
from src import queries, utils, connections, transforms

# Directories
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               
DIR_DATA = os.getenv("DIR_DATA")   
DIR_TEXT_RAW = os.path.join(DIR_DATA, 'text', 'raw')

# Load Configuration Files                                                      
CONFIG_CONN = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config

# Get List of Files
files = os.listdir(DIR_TEXT_RAW)
                                                                                
# Connection Configurations
load_dotenv()
HOST = CONFIG_CONN['MYSQL']['HOST']                                             
USER = CONFIG_CONN['MYSQL']['USER']                                             
PASSWORD = os.getenv('MYSQL_PASSWORD')                                     
PORT = CONFIG_CONN['MYSQL']['PORT']                                             
DATABASE = CONFIG_CONN['MYSQL']['DATABASE']                                     
                                                
# Other Globals
TABLE_NAME = "filing_index"

# Establish Connection to MySql                                                 
client = connections.MysqlClient().get_client(                                  
    host=HOST,                                                                  
    user=USER,                                                                  
    password=PASSWORD,                                                          
    port=PORT,                                                                  
    database=DATABASE                                                           
)  

# Check If Index Table Contains Data
test_df, test_status, test_error = queries.query_get_all_filing_index(client)
if test_df.shape[0]:
    queries.delete_all_from_table(TABLE_NAME, client)
else:
    print("Filing index table empty.  Proceeding with insertions")

# Load Files
patterns = {
        "CIK": "CENTRAL INDEX KEY:.*\n",
        "FILING_TYPE": "CONFORMED SUBMISSION TYPE:.*\n",
        "FILING_DATE": "FILED AS OF DATE:.*\n",
        "COMPANY_NAME": "COMPANY CONFORMED NAME:.*\n",
        "CIK": "CENTRAL INDEX KEY:.*\n",
        "IRS_NUMBER": "IRS NUMBER:.*\n",
}

# Create Index Filing Pandas Dataframe
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


