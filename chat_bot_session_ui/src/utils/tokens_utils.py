from .custom_logger import Logger 
from typing import Dict
import tiktoken 


#This class will be used to keep track of the number of token for each system and user prompt
#for now we only handle modal_type equal text-to-text
class TokenCounter : 
    def __init__(self,model:str,logger:Logger,modal_type:str="text-to-text") : 
        """
        model : str = the model set on the LLMCall object 
        modal_type : str = modal type of the LLMCall (for now we only handle text-to-text)
        """
        self.model = model 
        self.modal_type = modal_type 
        self.token_count = []
        self.encoding = tiktoken.encoding_for_model(model) 
        self.logger = logger 
    def append_new_prompt_pair(self,prompt : Dict) : 
        """
        This function will take a pair of (system_prompt,user prompt) or (user_prompt), compute the number of token \
        for each each prompt and append them to token_count
        """

        if len(prompt) == 2 : 
            system_prompt_tokens_count = self.encoding.encode(prompt["system"])
            user_prompt_token_count = self.encoding.encode(prompt["user"])
            self.token_count.append({
                "system_prompt" : prompt["system"], 
                "system_prompt_tokens_count" : system_prompt_tokens_count,
                "user_prompt" : prompt["user"],
                "user_prompt_token_count" : user_prompt_token_count
            })
            self.logger.info(f"System prompt : \n{prompt["system"]}",True)
            self.logger.info(f"Number of tokens of system prompt : {system_prompt_tokens_count}")
            self.logger.info(f"User prompt : \n {prompt["user"]}")
            self.logger.info(f"Number of tokens for user prompt : {user_prompt_token_count}")
            
            
            
        elif len(prompt) == 1 : 
            user_prompt_token_count = self.encoding.encode(prompt["user"])
            self.token_count.append({
                "user_prompt" : prompt["user"],
                "user_token_count" : user_prompt_token_count
            })
            self.logger.info(f"User prompt : \n {prompt["user"]}")
            self.logger.info(f"Number of tokens for user prompt : {user_prompt_token_count}")
        else : 
            raise ValueError("new prompt pair have an incorrect size") 
        


