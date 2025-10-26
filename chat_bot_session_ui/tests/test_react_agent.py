from chat_bot_session_ui.src.agents.patterns.react_agent import  ReactAgent
from chat_bot_session_ui.src.utils.custom_logger import Logger
from chat_bot_session_ui.src.utils.env_utils import load_env
from chat_bot_session_ui.src.utils.tests_utils import create_txt_file_in_tests
from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader, LLMCall
from chat_bot_session_ui.src.tools.web_search_tools import TavilySearchTool
import os 



# def test_react_agent_without_streaming() : 
#     print("### start test react agent without streaming ###")
#     logger_file_path = create_txt_file_in_tests("react_agent_without_streaming.txt")
#     logger = Logger(logger_file_path) 
#     with  load_env(["OPENAI_API_KEY_TEST"]) : 
#         key = os.environ.get("OPENAI_API_KEY_TEST") 
#         llm_data_loader = LLMDataLoader(model="gpt-4",api_key=key,llm_spec={})
#         llm_call = LLMCall(llm_data_loader=llm_data_loader,logger=logger)
#         react_agent = ReactAgent(llm_call=llm_call, tools=[TavilySearchTool], 
#                                  logger=logger )
#         res = react_agent.pipeline("who won the men's 2020 wimbeldon championship")
#         for step in res : 
#             print(step) 

#         print("### end test react agent without streaming ###")

def test_react_agent_with_streaming() : 
    print("### start test react agent without streaming ###")
    logger_file_path = create_txt_file_in_tests("react_agent_wit_streaming.txt")
    logger = Logger(logger_file_path) 
    with load_env(["OPENAI_API_KEY_TEST"]) : 

        key = os.environ.get("OPENAI_API_KEY_TEST") 
        llm_data_loader = LLMDataLoader(model="gpt-4",api_key=key,llm_spec={"stream":True})
        llm_call = LLMCall(llm_data_loader=llm_data_loader,logger=logger)
        react_agent = ReactAgent(llm_call=llm_call, tools=[TavilySearchTool], 
                                     logger=logger )
        streamed_response = react_agent.think_with_stream("is physics a science field")
        print("streamed response type")
        print(type(streamed_response))
        print("\n\n")

        for token in streamed_response :
                print(token,end="",flush=True)






    print("### end test react agent without streaming ###")
    

