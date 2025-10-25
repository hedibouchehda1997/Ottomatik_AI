from src.agents.prompts.tool_calling_prompts import tool_calling_sys_prompt, tool_calling_response_generator
from src.models.llm_models import LLMCall, LLMDataLoader
from src.utils.custom_logger import Logger 
from src.tools.tools import Tool 
from typing import Dict, List
import re 
import json 

class ToolCallingAgent : 
    def __init__(self,llm_call:LLMCall, tools:List[Tool], system_prompt:str, logger:Logger, name:str = "tool_calling_agent" ) :
                
        if llm_call is None : 
            raise ValueError("you need to provide APILLMCall") 
        else : 
            self.llm_call = llm_call 
        if tools is None or len(tools) == 0 : 
            raise ValueError("you need to provide tools for the toll calling chat bot")
        else : 
            self.tools = tools 
        # self.memory = memory

        self.system_prompt = system_prompt
        self.thinking_res = ''
        self.name = name 
        self.logger = logger
        
        self.history_action = "" 
        self.tools_description = ""
        for tool in tools : 
            tool_description = tool.get_tool_details() 
            self.tools_description += tool_description + "\n"

        self.sys_prompt = tool_calling_sys_prompt.format(system_prompt=system_prompt,tool_description=self.tools_description) 
    
    def think(self,query:str) : 
        messages = [{"role":"system","content":self.sys_prompt},
                    {"role":"user","content":f"User query : {query}"}] 
        self.thinking_res = self.llm_call(messages) 
        
        if isinstance(self.thinking_res,str) : 
            print("no streaming mode ")


    def get_sys_prompt(self) : 
        return self.sys_prompt  

    def set_sys_prompt(self,system_prompt:str) : 
        self.sys_prompt = system_prompt
         

    def ParseThinking(self) : 
        # print("start parsing")
        pattern = r"<response>(.*?)</response>"
        match_response = re.search(pattern,self.thinking_res,re.DOTALL) 
        if match_response :
            # print("response ")
            res = match_response.group(1) 

            return res
        pattern = r"<action>(.*?)</action>" 
        match_action = re.search(pattern,self.thinking_res,re.DOTALL) 
        if match_action : 
            # print("case of tool call")
            tool_call = {}
            res = match_action.group(1) 
            pattern = r"<name>(.*?)</name>" 
            tool_name_match = re.search(pattern,self.thinking_res,re.DOTALL) 
            if tool_name_match :  
                # print("find tool name ")
                tool_name = tool_name_match.group(1) 
                tool_call["name"] = tool_name.strip()
            pattern = r"<inputs>(.*?)</inputs>"
            inputs_match = re.search(pattern,self.thinking_res,re.DOTALL) 
            if inputs_match :  
                # print("find input dict")
                inputs = json.loads(inputs_match.group(1))   
                tool_call["inputs"] = inputs  
                return tool_call
        if match_response is None and match_action is None : 
            #bad output format 
            # print("bad output format ")
            pass 

    def act(self,action_dict:Dict[str,str]) : 
        # print("start running action")
        func_name = action_dict["name"]
        self.logger.info(f"running the following tool : {func_name} \n")
        tool_to_execute = None 
        for tool in self.tools : 
            if func_name == tool.name : 

                tool_to_execute = tool 
                break 
        if tool_to_execute is None : 
            self.logger.error(f"failed to find the tool named : {func_name} \n")
            return False 
        else : 
            response = tool_to_execute.run(action_dict["inputs"])
            self.logger.info(f"Tool running output : \n {response} \n")
            return response 
    def response_generator(self,query:str,tool_call_details:str) : 
        full_prompt = tool_calling_response_generator.format(query=query, tool_call_details=tool_call_details)
        messages = [{"role":"user","content":f"{full_prompt}"}]
        response = self.llm_call(messages) 
        self.logger.info(f"{self.name} agent final response : \n {response}\n")
        return response 


    def __call__(self,query:str) : 
        print("calling tool from tool calling agent ")
        self.logger.info( f"Calling agent : {self.name} \n") 
        self.logger.info( f"User query : {query} \n")
    
        self.think(query) 

        res_thinking  = self.ParseThinking() 
        print(".....type of res_thinking")
        print(type(res_thinking))

        if isinstance(res_thinking,str)  : 
            print("got final response from the details ")
            pass 
        elif isinstance(res_thinking,Dict) :
            act_response = self.act(res_thinking) 
            tools_details = f"""
{json.dumps(res_thinking)} 
{act_response}
            """.strip()
            final_response = self.response_generator(query,tools_details)
            print("final respone")
            print(final_response)

