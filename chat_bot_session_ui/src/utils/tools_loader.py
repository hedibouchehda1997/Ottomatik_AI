from typing import Dict, List  
from chat_bot_session_ui.src.tools.tools import Tool 



class ToolsLoader :  
    def __init__(self) :
        self.list_tools = [] 


    def add_tool(self, tool:Tool) : 
        self.list_tools.append(tool)

    def run_tool(self,tool_details:Dict) : 
        for tool in self.list_tools : 
            if tool.name == tool_details["name"] : 
                tool_response = tool.run(tool_details["inputs"])
                return tool_response

    # def set_tools(self,list_tools : List[Tool]) : 
    #     self.list_tools = list_tools 
    
  

    def get_tools_description(self) : 
        res = [] 
        for tool in self.list_tools :  
            res.append(tool.get_tool_details_dict()) 
        return res 


