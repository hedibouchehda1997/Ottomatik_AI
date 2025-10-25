from typing import Callable, Dict


#it's the tool that will be used in function calling llm pipelines
class Tool : 
    def __init__(self,name:str,description:str,func:Callable) : 
        """
        name : the name with which the function will be refered to 
        description of the function : explaining what it does and the inputs and outputs 
        func : the function that will be executed 
        """
        self.name = name 
        self.description = description 
        self.func = func 
    
    def get_tool_details(self) : 
        return "name : "+self.name + "\n" + "description : \n"+self.description
          
    def run(self,inputs:Dict[str,str]) : 
        """
        call the method related to the tool 
        inputs : Dict[str,str] = contains the inputs of the method
        """
        response = self.func(**inputs) 
        return response 