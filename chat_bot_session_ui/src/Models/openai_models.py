#Overall explanation : 
    #Here we declare the different pipelines of OpenAI sdk. For example the ones used to do queries on models like gpt and other sdk for multi-modal input\output

from typing import Dict, List
from src.utils.custom_logger import Logger
from src.utils.tokens_utils import TokenCounter 
from openai import OpenAI

#This class will be used to do queries on gpt models 
class GPTCall : 
    def __init__(self,model_specs:Dict,token_counter:TokenCounter,logger:Logger) : 
        if "model" not in model_specs : 
            raise ValueError("the gpt is not set with a model") 
        if "api_key" not in model_specs :
            raise ValueError("you didn't provide an OpenAI key")
        self.call_input = model_specs 
        self.token_counter = token_counter 
        self.logger = logger
        self.gpt_client = OpenAI(api_key=self.call_input["api_key"])
        self.call_input.pop("api_key",None)


    def __call__(self,messages:List[Dict]) : 
        """
        This method that will be called to do the api call  
        the inputs : 
            messages : List[Dict] = a list of two dict. Every dict contain the role (user or sys) and the content
        """


        self.logger.info(f"calling : {self.call_input["model"]}")
        self.call_input["messages"] = messages  
        sys_user_prompt_pair = {}
        for message in messages :
            sys_user_prompt_pair[message["role"]] = message["content"]
        self.token_counter.append_new_prompt_pair(sys_user_prompt_pair)
        try : 
            print("parameters on gpt call ") 
            print(self.call_input)
            response = self.gpt_client.chat.completions.create(**self.call_input) 
            print("response") 
            print(type(response))
            if isinstance(response,str) : 
                return response.choices[0].message.content.strip()
            else : 
                return response 
        except Exception as e :  
            print(f"{e}")
            self.logger.error(f"error calling model : {e}")





        

        
        


