import logging                                                                     
import os
import git                                                                         
import yaml                                                                        
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


def check_table_exists(cursor: CMySQLCursor, table: str, database: str) -> bool:             
    """                                                                            
    Check if table exists in database.                                             
    """                                                                         
    print("Checking if table {} exists in database {}".format(table, database))
    response = False                                                            
    query = """
        USE {};

        SELECT COUNT(*)                                                            
        FROM information_schema.tables                                             
        WHERE TABLE_NAME = '{}';                                                   
        """.format(database, table)                                                     
    try:                                                                           
        response = cursor.execute(query)
        cursor.close()
        print(f"Tables Found => {response}")
    except Exception as e:
        print(f"Error occured while check if table exists {e}")
        response = False

    return True if response else False






