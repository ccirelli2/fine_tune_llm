import logging                                                                     
import re
import os
import git                                                                         
import yaml                                                                        
import pandas as pd
from mysql.connector.cursor_cext import CMySQLCursor 

logging.basicConfig(level=logging.INFO)                                            
logger = logging.getLogger(__name__)                                               
logger.setLevel(level="INFO")                                                      
                                                                                   

def get_root_directory():
    directory = git.Repo(".", search_parent_directories=True).working_tree_dir
    assert os.path.exists(directory), "Root directory does not exist"
    print(f"Returning root directory as {directory}")
    return directory


class LoadConfig:                                                                  
    def __init__(self):                                                            
        self.directory = ""                                                        
        self.file_name = ""                                                        
        self.config = {}                                                           
        logger.info(f"{__class__} instantiated successfully")                      
                                                                                   
    def load(self, file_name: str, directory: str) -> dict:                        
        """ """                                                                    
        assert file_name.split(".")[-1] == "yaml", "file ext must be yaml"         
        path = os.path.join(directory, file_name)                                  
        logger.info("Loading config file => {}".format(file_name))                 
        with open(path, "r") as f:                                                 
            self.config = yaml.load(f, Loader=yaml.FullLoader)                     
        logger.info("Returning config")                                            
        return self


def check_database_exists(cursor: CMySQLCursor, db_name: str) -> bool:
    """
    """
    exists = False
    query = """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME = '{}';
        """.format(db_name)
    cursor.execute(query)
    response = cursor.fetchall()
    print("Response => {}".format(response))
    if response[0][0] > 0:
        exists = True
    return exists

def check_table_exists(cursor: CMySQLCursor, table: str, database: str) -> bool:             
    """                                                                            
    Check if table exists in database.                                             
    """                                                                         
    print("Checking if table {} exists in database {}".format(table, database))
    exists = False                                                            
    query = """
        SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_NAME = '{}';
        """.format(table)
    try:                                                                           
        cursor.execute(query)
        response = cursor.fetchall()
        print(f"\tRaw response => {response}")
        if response[0][0] != 0:
            exists = True
        print(f"\tTables Exists => {exists}")
    except Exception as e:
        print(f"\tError occured while check if table exists {e}")
    
    return exists


class TrialParamAccumulator:                                                       
    """                                                                            
    """                                                                            
    def __init__(self, trial_id: str):
        self.trial_id = trial_id
        self.parameters = {}                                                                
        self.index = 0                                                                      
        print(f"{__class__} instantiated successfully")                            
                                                                                   
    def get_dataframe(self):                                                       
        return pd.DataFrame(self.parameters).transpose()                           
                                                                                   
    def log(self, name: str, value: str, category: str = "",        
            dtype: str = "string"):                                                
        """                                                                        
        """                        
        self.parameters[self.index] = {                                            
            "name": name, "value": value, "trial_id": self.trial_id,                    
            "category": category, "datatype": dtype                                
        }                                                                          
        self.index += 1                                                            
        return self


def normalize_financial_metric_names(name: str):                                   
    """                                                                            
    Validation dataset financial metric names are concatenated strings.            
    We need to maintain the original names so that we can join the ground truth 
    data.                                                                          
    For the LLM we need to split the names on capital Letters.                     
                                                                                   
    Example:                                                                       
        NetIncome => Net Income                                                    
                                                                                   
    Regex:                                                                         
        replace any capital letter with a space and then the same capital letter
    """                                                                            
    print("Normalizing financial Parameter => {}".format(name))                                           
    name = re.sub(r'([A-Z])', r' \1', name)                                        
    print("Result => {}".format(name))                                             
    return name     


