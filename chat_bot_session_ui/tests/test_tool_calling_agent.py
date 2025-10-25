from chat_bot_session_ui.src.agents.patterns.tool_calling_agent import  ToolCallingAgent
from chat_bot_session_ui.src.utils.custom_logger import Logger
from chat_bot_session_ui.src.utils.env_utils import load_env
from chat_bot_session_ui.src.utils.tests_utils import create_txt_file_in_tests
from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader, LLMCall
from chat_bot_session_ui.src.tools.web_search_tools import TavilySearchTool
import os

def test_tool_calling_agent_without_streaming() : 
    print("### start test calling agent without streaming ###")
    logger_file_path = create_txt_file_in_tests("tool_calling_agent_test_without_streaming.txt")
    logger = Logger(logger_file_path) 
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST") 
        print("printing the key") 
        llm_data_loader = LLMDataLoader(model="gpt-4",api_key=key,llm_spec={})
        llm_call = LLMCall(llm_data_loader=llm_data_loader,logger=logger)
        tool_calling_agent = ToolCallingAgent(llm_call=llm_call, tools=[TavilySearchTool], 
                                              system_prompt="you are a helpful assistant", 
                                              logger=logger)
        first_query =  "is physics a field of science"
        tool_calling_agent(first_query) 
        print("\n\n\n")
        second_query = "who won ufc 311" 
        tool_calling_agent(second_query)

        

        
        

    print("### end test calling agent without streaming ###")

