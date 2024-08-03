"""
Script containing prompt & query templates & retrieval functions
"""
from datetime import datetime


###############################################################################
# QUERY TEMPLATES
###############################################################################

def query_single_attribute(name: str, conditions: dict = None):
    """
    Simple function to retrieve a given financial statement field.

    Ex: Net Income.

    Also can add conditions as like year: 2021
    """
    query = f"Financial Statement Field {name}"
    if conditions:
        for c in conditions:
            query = query + f" {c} {conditions[c]}"
    return query

def prompt_simple(date_today: str, context: list, task: str, example: str) -> str:
    """
    """
    today = datetime.today().strftime("%B %d, %Y")

    prompt = """                                                                       
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>                        
        Today Date: {}                                                            
                                                                                           
        You are a helpful Assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>  
                                                                                        
        Here is a body of text {}.                                                     
        Please {}.                                                                      
        Return your answer in json format.                                              
        Here is an example {}.                                                          
                                                                                        
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>                         
    """.format(today, "\n".join(context), task, example)                                   
                                                  
    return prompt


