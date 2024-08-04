"""
Test using pandas to insert data into Mysql
"""
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src import utils

# Directories                 
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               
DIR_DATA = os.getenv("DIR_DATA")                                              
DIR_DATA_VAL = os.path.join(DIR_DATA, 'validation', 'clean')

# Config Files                                                                     
CONFIG_MYSQL = utils.LoadConfig().load(file_name="connections.yaml", directory=DIR_CONFIG).config
                                                                                   
# MySQL - Connection                                                               
HOST = CONFIG_MYSQL['MYSQL']['HOST']                                               
USER = CONFIG_MYSQL['MYSQL']['USER']                                               
PASSWORD = os.getenv("MYSQL_PASSWORD")                                       
PORT = CONFIG_MYSQL['MYSQL']['PORT']                                               
DATABASE = CONFIG_MYSQL['MYSQL']['DATABASE']
TABLE = "validation_sub"
conn = create_engine(
        f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
        pool_size=20, max_overflow=0
)

# Files
FILE_NAMES = [
#        "num",
#        "pre",
#        "sub",
        "tag"
]
COLUMN_CONFIG = {                                                                  
    "num": ["adsh", "tag", "version", "coreg", "ddate", "qtrs", "uom", "value", "footnote"],
    "pre": ["adsh", "report", "line", "stmt", "inpth", "rfile", "tag", "version",
        "plabel", "negating"],                                                     
    "sub": ["adsh","cik","name","sic","countryba","stprba","cityba","zipba",       
        "bas1","bas2", "baph", "countryma","stprma", "cityma","zipma","mas1",   
        "mas2","countryinc", "stprinc","ein","former","changed","afs","wksi",   
        "fye","fye","form","period", "fy","fp","filed","accepted","prevrpt",       
        "detail","instance","nciks","aciks"],                                      
    "tag": ["tag", "version", "custom", "abstract", "datatype", "iord", "crdr", 
        "tlabel", "doc"],                                                      
}   
TABLE_CONFIG = {
    "num": "validation_num",
    "pre": "validation_pre",
    "sub": "validation_sub",
    "tag": "validation_tag"
}
# Iterate FileNames
for name in FILE_NAMES:
    
    # Construct Data Paramaters
    file_name = "{}.csv".format(name)
    columns = COLUMN_CONFIG[name]
    table = TABLE_CONFIG[name]

    # Load Data
    print("Load File {}".format(file_name))
    data = pd.read_csv(os.path.join(DIR_DATA_VAL, file_name), usecols=columns)
    print("Data shape => {}".format(data.shape))
    print("Data Columns => {}".format(data.columns)) 
    
    # Insert Data
    chunksize = 10_000
    print("Inserting Data to Database {} Table {}".format(DATABASE, table))

    for start in range(0, data.shape[0], chunksize):
        end = start + chunksize
        df_chunk = data.iloc[start: end]
        print("\tInserting from {} to {} of {}".format(start, end, data.shape[0]))
        df_chunk.to_sql(table, con=conn, if_exists='append', index=False)
        print("\tInsertion completed")

    print("Script completed successfully")

