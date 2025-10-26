from src.agents.prompts.react_prompts import react_prompt 
from src.models.llm_models import LLMCall, LLMDataLoader
from src.utils.custom_logger import Logger 
from src.tools.tools import Tool 
from typing import Dict, List
import time
import re 
import json 


class ReactAgent : 
    def __init__(self,llm_call:LLMCall, tools:List[Tool],
                logger:Logger, name="react_agent", max_iteration:int=12,
                human_in_loop=False) : 
        if llm_call is None : 
            raise ValueError(f"{name} need a model") 
        else : 
            self.llm_call = llm_call 

        if tools is None or len(tools) == 0 : 
            raise ValueError("you need to provide tools for the react agent")
        else : 
            self.tools = tools  

        self.name = name 
        self.current_iteration = 0 
        self.history_action = "" 
        self.tools_description = "" 
        self.max_iteration = max_iteration 

        for tool in tools : 
            tool_description = tool.get_tool_details() 
            self.tools_description += tool_description + "\n"
        self.end_reasoning = False 

    def parse_llm_response(self,llm_response ) : 
        res_if_good = {}
        pattern = r"<action>(.*?)</action>" 
        match = re.search(pattern ,llm_response,re.DOTALL) 
        if  match  :
            detail = match.group(1) 
            pattern = r"<name>(.*?)</name>" 
            match = re.search(pattern,detail,re.DOTALL)  
            if match :
                res_if_good["name"] = match.group(1).strip()
                pattern = r"<inputs>(.*?)</inputs>" 
                match = re.search(pattern,detail,re.DOTALL)
                if match : 
                    try : 
                        input_dict = json.loads(match.group(1)) 
                        res_if_good["inputs"] = input_dict
                        return res_if_good
                    except json.JSONDecodeError as e : 
                        print("the tool input dict is not formatted correctly")        
                else : 
                    return False 
                    
            else : 
                return False  


        else :
            pattern = r"<answer>(.*?)</answer>"
            match = re.search(pattern ,llm_response,re.DOTALL) 
            if match : 
                res_if_good["answer"] = match.group(1) 
                return res_if_good
            else : 
                return False  


     
    def think(self,query:str) :  
        self.logger.info(f"{self.name} starts thinking \n")
        full_prompt = react_prompt.format(query=query,tools=self.tools_description, history_action=self.history_action)

        messages = [{"role":"user","content":full_prompt}]
        
        thinking_result = self.llm_call(messages) 
        # self.logger.info(f"LLM response :\n {thinking_result}")
        # print("printing the llm call response ")
        # print(thinking_result) 
        input_dict = self.parse_llm_response(thinking_result)
    

#         print(input_dict)
#         result = self.act(input_dict) 
#         print(result)
        if self.current_iteration > self.max_iteration : 
            print("we reached the maximum of iterations")
            result = "we attained the maximum number of iteration allowed. Here's the reasoning so far :\n"+self.history_action
            self.logger.warning(result)
            self.end_reasoning = True 
            return result, False 
        else :
            if "name" in list(input_dict.keys()) :  
                act_res = self.act(input_dict) 
                if isinstance(act_res,bool) : 
                    print("action wasn't executed correctly. Retrying ") 
                    self.think(query)
                elif isinstance(act_res,str) : 
                    self.current_iteration += 1
                    name = ""
                    if self.human_in_loop : 
                        name = input("Human feedback : ") 
                           
                    step_for_history = self.ParseForHistory(input_dict,act_res,name)
                    self.history_action += step_for_history + "\n" 

                    print("returning a step ")
                    return step_for_history, "step" 
            if "answer" in list(input_dict.keys()) :
                    print("returning final value ") 
                    return input_dict["answer"], "final"
                    self.end_reasoning = True



