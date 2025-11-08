from chat_bot_session_ui.src.models.llm_models import LLMCall, LLMDataLoader
from chat_bot_session_ui.src.utils.custom_logger import Logger 
from typing import Dict, List


class SimpleAgent : 
    def __init__(self,llm_call:LLMCall, logger:Logger, name="simple_agent",system_prompt:str="") : 
        if llm_call is None : 
            raise ValueError(f"{name} need a model") 
        else : 
            self.llm_call = llm_call  


        self.name = name 
        self.system_prompt = system_prompt
    


    def __call__(self,user_query:str) :

        messages =  [{"role":"system","content":self.system_prompt},
                     {"role":"user","content":user_query}] 

        return self.llm_call(messages) 


    def set_system_prompt(self,system_prompt:str) : 
        self.system_prompt = system_prompt

