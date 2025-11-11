from typing import Dict, List 
from chat_bot_session_ui.src.agents.patterns.react_agent import ReactAgent 
from chat_bot_session_ui.src.agents.patterns.tool_calling_agent import ToolCallingAgent
from chat_bot_session_ui.src.tools.web_search_tools import TavilySearchTool
from chat_bot_session_ui.src.utils.custom_logger import Logger
from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader, LLMCall
from chat_bot_session_ui.src.utils.env_utils import load_env
from chat_bot_session_ui.src.memories.simple_memory import SimpleMemory
from chat_bot_session_ui.src.agents.patterns.simple_agent import SimpleAgent
import os


class AgentFactory : 
    def __init__(self) : 
        self.agent_details = None 
        self.tools = []
        pass 

    def set_agent_details(self,agent_details : Dict) : 
        self.agent_details = agent_details  

    def get_agent_details(self) : 
        return self.agent_details  

    def fetch_tools(self,tool_names:List[str]) : 
    
        for tool_name in tool_names :
            if tool_name == "tavily_search" : 
                self.tools.append(TavilySearchTool)

    def build_llm_model(self) : 
        if self.agent_details["model"].startswith("gpt") : 
            with load_env(["OPENAI_API_KEY"])   : 
                self.logger = Logger("test.txt")
                key = os.environ.get("OPENAI_API_KEY") 
                self.llm_data_loader = LLMDataLoader(model=self.agent_details["model"],
                                            api_key=key , 
                                            llm_spec = {"stream":True}) 
                self.llm_call = LLMCall(llm_data_loader=self.llm_data_loader,  
                                        logger=self.logger)

    def build_agent(self) : 
        self.build_llm_model()
        if self.agent_details["agent_type"] == "react" : 
            self.fetch_tools(self.agent_details["tools"])
            self.agent = ReactAgent(llm_call=self.llm_call, 
                                    tools=self.tools, 
                                    logger = self.logger)
        elif self.agent_details["agent_type"] == "tool_calling" : 
            print("we're building a tool calling agent")
            self.fetch_tools(self.agent_details["tools"])
            tool_calling_agent = ToolCallingAgent(llm_call=self.llm_call, tools=self.tools,
                                                  system_prompt=self.agent_details["system_prompt"],
                                                  logger = self.logger) 

            return tool_calling_agent 
            
        elif self.agent_details["agent_type"] == "chat_bot" : 
            simple_memory = SimpleMemory()

            simple_agent = SimpleAgent(llm_call=self.llm_call, logger=self.logger, 
                                        simple_memory=simple_memory, system_prompt=self.agent_details["system_prompt"],
                                        name=self.agent_details["agent_name"])  

            return simple_agent

