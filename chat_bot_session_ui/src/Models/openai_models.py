#Overall explanation : 
    #Here we declare the different pipelines of OpenAI sdk. For example the ones used to do queries on models like gpt and other sdk for multi-modal input\output

from typing import Dict, List
from src.utils.custom_logger import Logger
from .llm_models import TokenCounter
from openai import OpenAI

#This class will be used to do queries on gpt models 
class GPTCall : 
    def __init__(self,model_specs:Dict,token_counter:TokenCounter) : 
        if "model" not in model_specs : 
            raise ValueError("the gpt is not set with a model") 
        if "api_key" not in model_specs :
            raise ValueError("you didn't provide an OpenAI key")
        self.call_input = model_specs 
        self.token_counter = token_counter 

    def __call__(self,messages:List[Dict]) : 
        """
        This method that will be called to do the api call  
        the inputs : 
            messages : List[Dict] = a list of two dict. Every dict contain the role (user or sys) and the content
        """
        self.call_input["messages"] = messages  
        if self.logger is not None : 
            sys_user_prompt_pair = {}
            for message in messages :
                sys_user_prompt_pair[message["role"]] = message["content"]
            self.token_counter.append_new_prompt_pair(sys_user_prompt_pair)
        try : 
            response = OpenAI.chat.completions.create(**self.call_input) 
            response = response.choices[0].message.content.strip()
            print("gpt call response") 
            print(response)
            
            return response
        except Exception as e :   
            self.logger.error(f"errr on the call : {e}") 


        

        
        


