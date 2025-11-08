from typing import Dict, List 
from chat_bot_session_ui.src.utils.agent_factory import AgentFactory 
from chat_bot_session_ui.src.utils.agent_loader import DataLoader, LLMPipelineSessionManager 


class SessionManager : 
    def __init__(self, user_id:str) : 
        self.agent_factory = AgentFactory() 
        