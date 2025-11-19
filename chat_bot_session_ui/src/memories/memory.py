

class Memory : 
    def __init__(self) : 
        self.query_response_pairs = [] 
    
    def add_system_prompt(self,system_prompt:str) : 
        self.system_prompt = system_prompt 

    def add_query_response_pair(self,user_query:str,ai_response:str) : 
        self.query_response_pairs.append({"user_query":user_query,"ai_response":ai_response}) 

    def dump(self) : 
        for query_response_pair in self.query_response_pairs :  
            print(query_response_pair) 
            print("**************")


        

    


