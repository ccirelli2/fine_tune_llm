import pandas as pd


class TrialParamAccumulator:                                                       
    """                                                                            
    """                                                                            
    def __init__(self):                                                            
        self.parameters = {}                                                            
        self.index = 0                                                                  
        print(f"{__class__} instantiated successfully")                           

    def get_dataframe(self):
        return pd.DataFrame(self.parameters).transpose()

    def log(self, name: str, value: str, trial_id: str, category: str = "",        
            dtype: str = "string"):                                                
        """                                                                        
        """                                                                        
        self.parameters[self.index] = {                                            
            "name": name, "value": value, "trial_id": trial_id,                    
            "category": category, "datatype": dtype                                
        }                                                                          
        self.index += 1                                                            
        return self 

param_logger = TrialParamAccumulator()

name = "chris"
value = "value"
trial_id = "1234"
category = "cat"
datatype = "string"

param_logger.log(name, value, trial_id, category, datatype)

name = "chris"
value = "value"
trial_id = "1234"
category = "cat"
datatype = "string"

param_logger.log(name, value, trial_id, category, datatype)

print(param_logger.get_dataframe())
