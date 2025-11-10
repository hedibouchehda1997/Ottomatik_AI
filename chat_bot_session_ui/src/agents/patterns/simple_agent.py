from chat_bot_session_ui.src.models.llm_models import LLMCall, LLMDataLoader
from chat_bot_session_ui.src.utils.custom_logger import Logger 
from chat_bot_session_ui.src.memories.simple_memory import SimpleMemory
from typing import Dict, List


class SimpleAgent : 
    def __init__(self,llm_call:LLMCall, logger:Logger, name="simple_agent",system_prompt:str=""
                ,simple_memory:SimpleMemory=None) : 
        if llm_call is None : 
            raise ValueError(f"{name} need a model") 
        else : 
            self.llm_call = llm_call  

        if name == "" or name is None : 
            self.name = "chat bot"
        else : 
            self.name = name 
        self.system_prompt = system_prompt
        self.simple_memory = simple_memory
    


    def __call__(self,user_query:str) :

        messages =  [{"role":"system","content":self.system_prompt},
                     {"role":"user","content":user_query}] 


        return self.llm_call(messages) 


    def set_system_prompt(self,system_prompt:str) : 
        self.system_prompt = system_prompt
        self.simple_memory.add_system_prompt(system_prompt)

    def add_query_response(self,user_query:str,ai_response:str) : 
        self.simple_memory.add_query_response_pair(user_query, ai_response)



