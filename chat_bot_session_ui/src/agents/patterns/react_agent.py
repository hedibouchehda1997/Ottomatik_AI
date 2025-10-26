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
        self.logger = logger 
        self.human_in_loop = human_in_loop

        for tool in tools : 
            tool_description = tool.get_tool_details() 
            self.tools_description += tool_description + "\n"
        self.end_reasoning = False 


    def parse_llm_response(self,llm_response ) : 
        res_if_good = {}
        print("******************llm_response ************")
        print(llm_response)
        pattern = r"<action>(.*?)</action>" 
        match = re.search(pattern ,llm_response,re.DOTALL) 
        if  match  :
            print("matchy matchy matchy matchy matchy !!!!! ")
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


    def act(self,action_dict:Dict[str,str]) : 
        # print("start running action")
        func_name = action_dict["name"]
        tool_to_execute = None 
        for tool in self.tools : 
            if func_name == tool.name : 
                self.logger.info(f"tool to execute : {func_name} \n")
                # print(f"tool to execute : {func_name}")
                tool_to_execute = tool 
                break 
        if tool_to_execute is None : 
            self.logger.error(f"failed to find the tool named : {func_name}")
            return False 
        else : 
            response = tool_to_execute.run(action_dict["inputs"])
            return response


    def ParseForHistory(self,action_dict,act_result,human_feedback="") : 
        result = "action : \n"
        result += "name : "+ action_dict["name"] +  "\n"
        result += "inputs : " + json.dumps(action_dict["inputs"])  +  "\n"
        result += "observation : " + act_result   +  "\n"
        if human_feedback != "" : 
            result += "user feedback : " + human_feedback +"\n"

        self.logger.info(f"Action and observation : \n {result} \n")
        # print("Parse for history") 
        # print(result) 
        return result 


     
    def think(self,query:str) :  
        self.logger.info(f"{self.name} starts \n")
        full_prompt = react_prompt.format(query=query,tools=self.tools_description, history_action=self.history_action)

        messages = [{"role":"user","content":full_prompt}]
        
        thinking_result = self.llm_call(messages) 
        # return thinking_result
        input_dict = self.parse_llm_response(thinking_result)

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
                    print("step for history ")
                    print(step_for_history)
                    
                    # self.history_action += step_for_history + "\n" 

        #             print("returning a step ")
        #             return step_for_history, "step" 
        #     if "answer" in list(input_dict.keys()) :
        #             print("returning final value ") 
        #             return input_dict["answer"], "final"
        #             self.end_reasoning = True



