"""
Standard functions for connecting to projects various services
"""
import mysql.connector
from sqlalchemy import create_engine


class MySqlAlchemyClient:
    def __init__(self):
        print(f"{__class__} instantiated successfully")

    @staticmethod                                                                  
    def get_client(host: str, user: str, password: str, port: int, database: str = ""):
        if database:
            print("Creating connection with database")
            client = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
                user, password, host, port, database)
            )
        else:
            print("Creating connection without database")
            client = create_engine('mysql+mysqlconnector://{}:{}@{}:{}'.format(
                user, password, host, port)
            )

        return client


class MysqlClient:                                                                 
    """                                                                            
    Connect to mysql database.                                               
    """                                                                            
    def __init__(self):                                                            
        """                                                                        
        Instantiate class.                                                         
        """
        print("{} class instantiated successfully".format(__class__))                   
    
    @staticmethod
    def get_client(host: str, user: str, password: str, port: int, database: str=""):
        """                                                                        
        ::host: ip address of service.                                             
        ::user:                                                                    
        ::token: authentication key                                                
        ::port:                                                                    
        ::database:                                                                
        """                                                                        
        print("\tCreating connection to edgar database")
        if database:
            conn = mysql.connector.connect(
                host=host,                                  
                port=port,                                  
                user=user,                                  
                password=password,                             
                database=database,                          
                # collation=collation
            )
        else:
            conn = mysql.connector.connect(
                host=host,                                  
                port=port,                                  
                user=user,                                  
                password=password,                             
            )
        if conn.is_connected():
            print("\tConnection established successfully") 
        else:
            print("Error connecting to mysql")
        return conn  
