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
    """ """
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
        """ """
        prompt = f"""                                                                       
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>                        
            Today Date: {{{self.today}}}

            You are a helpful assistant tasked with extracting data from SEC Edgar filings.
            You will be given one or more pieces of text from company filings
            from which you need to extract a given financial attribute.
            <|eot_id|><|start_header_id|>user<|end_header_id|>

            Here is the body of text {{{self.context}}}.

            Please {{{self.task}}}.                                                        
            
            Return your answer in json format.                                              
            
            Here is an example of the expected response format {{name: value}}.
        
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>                         
        """
        return prompt


class ConstructPromptWithRational:
    def __init__(self, context: str, task: str):
        """
        Args
            context: data returned from knowledge store.
            task: extraction task that the llm is to perform.
            year: the year for which the llm is to return the value.
            example: an example of the output.
        """
        self.context = context
        self.task = task
        self.today = datetime.today().strftime("%B %d, %Y")
        print(f"{__class__} instantiated successfully")

    def build(self):
        """ """
        prompt = f"""                                                                       
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>                        
            Today Date: {{{self.today}}}

            You are a helpful assistant tasked with extracting data from SEC Edgar filings.
            You will be given one or more pieces of text from a companies
            SEC Edgar filings and are expected to return one or more
            numeric financial metrics. 
            
            <|eot_id|><|start_header_id|>user<|end_header_id|>

            Here is the body of text {{{self.context}}}.

            Please {{{self.task}}}.                                                        
            
            Below are the fields you need to return:
            1. field-name: the name of the field you are being asked to return.
            2. field-value: the numeric value of the field you are being asked to return.
            3. units: the unit of the field (example: thousands, millions, etc.).
            4. explanation: explain the steps you took to arrive at your answer.
            5. text: the paragraph of text where you found the field-value

            Please ensure to repond in json format.
            
            Here is an example response:
                {{
                field-name: name,
                field-value: numeric value,
                units: unit-value,
                text: paragraph,
                explanation: your-explanation,
            }}.
            
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>                         
        """
        return prompt


    claude_generated_prompt = """
    You are an AI assistant tasked with extracting specific attributes from SEC Edgar filings. Your goal is to accurately identify and extract the requested attribute from the given text. Follow these instructions carefully:
    1. You will be provided with the following inputs:
       <TEXT>
       {{TEXT}}
       </TEXT>

       <ATTRIBUTE>
       {{ATTRIBUTE}}
       </ATTRIBUTE>

    2. Carefully read and analyze the provided TEXT. Pay attention to both narrative text and any tables that may be present.
    
    3. Look for the specific ATTRIBUTE mentioned. This attribute could be a financial metric, a company detail, or any other relevant information typically found in SEC filings.

    4. When you find information related to the ATTRIBUTE, consider the context and ensure it is the most relevant and accurate representation of the requested attribute.

    5. If you find multiple instances of the ATTRIBUTE, choose the most recent or most relevant one, unless otherwise specified.

    6. If the ATTRIBUTE is not explicitly stated but can be inferred or calculated from the given information, do so and explain your reasoning.

    7. If you cannot find the ATTRIBUTE or there isn't enough information to infer it, indicate that the attribute was not found.

    8. Format your response as a JSON object with the following structure:
       {
         "attribute": "The name of the attribute you were asked to find",
         "value": "The extracted value of the attribute",
         "location": "A brief description of where in the text you found the information",
         "logic": "An explanation of how you arrived at your answer, including any calculations or inferences made"
       }

    9. Ensure that the "value" field in your JSON response is appropriate for the attribute. For example, if it's a numerical value, provide it as a number without currency symbols or commas. If it's a textual value, provide it as a string.

    10. In the "location" field, be as specific as possible. For example, "In the third paragraph under the 'Financial Results' section" or "In the 'Income Statement' table, second row".

    11. In the "logic" field, explain your reasoning process. If you made any assumptions or calculations, detail them here. If the attribute was explicitly stated, you can simply say so.

    12. If you couldn't find the attribute, your JSON response should look like this:
        {
          "attribute": "The name of the attribute you were asked to find",
          "value": null,
          "location": "Not found",
          "logic": "The requested attribute could not be found in the provided text. [Include any additional explanation if relevant]"
        }

    Remember, accuracy is crucial. Take your time to thoroughly analyze the text and provide the most precise and relevant information possible.

    """
