from typing import Dict, List  
from chat_bot_session_ui.src.tools.tools import Tool 



class ToolsLoader :  
    def __init__(self) :
        self.list_tools = None 


    def set_tools(self,list_tools : List[Tool]) : 
        self.list_tools = list_tools 
  

    def get_tools_description(self) : 
        res = [] 
        for tool in self.list_tools :  
            res.append(tool.get_tool_details_dict()) 
        return res 


