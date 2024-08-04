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


def task_single_attribute(name: str, conditions: dict = None):
    """
    """
    task = "Find {}".format(name)
    if conditions:
        for c in conditions:
            task = task + f" {c} {conditions[c]}"

    return task


class ConstructPromptSimple:
    def __init__(self, context: str, task: str, example: str = None):
        """
        Args
            context: data returned from knowledge store.
            task: extraction task that the llm is to perform.
            year: the year for which the llm is to return the value.
            example: an example of the output.
        """
        self.context = context
        self.task = task
        self.example = example
        self.today = datetime.today().strftime("%B %d, %Y")
        print(f"{__class__} instantiated successfully")

    def build(self):
        """
        """
        prompt = f"""                                                                       
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>                        
            Today Date: {{{self.today}}}

            You are a helpful Assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

            Here is a body of text {{{self.context}}}.

            Please {{{self.task}}}.                                                        
            
            Return your answer in json format.                                              
            
            Here is an example of the expected response format {{name: value}}.
        
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>                         
        """
        return prompt

class ConstructPromptWithRational:
    def __init__(self, context: str, task: str, example: str = None):
        """
        Args
            context: data returned from knowledge store.
            task: extraction task that the llm is to perform.
            year: the year for which the llm is to return the value.
            example: an example of the output.
        """
        self.context = context
        self.task = task
        self.example = example
        self.today = datetime.today().strftime("%B %d, %Y")
        print(f"{__class__} instantiated successfully")

    def build(self):
        """
        """
        prompt = f"""                                                                       
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>                        
            Today Date: {{{self.today}}}

            You are a helpful Assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

            Here is a body of text {{{self.context}}}.

            Please {{{self.task}}}.                                                        
            
            Return your answer in json format.                                              
            
            Here is an example of the expected response format
                {{financial-field: financial-value, rational: your-explanation}}.
        
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>                         
        """
        return prompt


