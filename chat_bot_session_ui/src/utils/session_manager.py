

class SessionManager : 
    def __init__(self,user_id) : 
        self.user_id = user_id 
        self.last_streamed_response = ""

    def set_agent(self,agent ) : 
        self.agent = agent