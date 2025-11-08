from chat_bot_session_ui.src.agents.patterns.simple_agent import  SimpleAgent 
from chat_bot_session_ui.src.utils.custom_logger import Logger
from chat_bot_session_ui.src.utils.env_utils import load_env
from chat_bot_session_ui.src.utils.tests_utils import create_txt_file_in_tests
from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader, LLMCall
import os 

def test_simple_agent_without_streaming() : 
    print("### start test simple agent without streaming ###")
    logger_file_path = create_txt_file_in_tests("simple_agent_without_streaming.txt") 
    logger = Logger(logger_file_path) 
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST") 
        llm_data_loader = LLMDataLoader(model="gpt-3.5-turbo",api_key=key,llm_spec={}) 
        llm_call = LLMCall(llm_data_loader=llm_data_loader, logger=logger) 
        simple_agent = SimpleAgent(llm_call=llm_call,logger=logger) 
        simple_agent.set_system_prompt("You are a helpful assistant, you respond in an concise way") 
        response = simple_agent("is it still woth it to invest time learning programming in the \
                     era of the AI") 

        if isinstance(response,str) : 
            print(f"the agent response : {response}") 
        else : 
            raise ValueError("the response is not in the correct type")



    print("### end test simple agent without streaming ###")

def test_simple_agent_with_streaming() : 
    print("### start simple agent with streaming ###")

    logger_file_path = create_txt_file_in_tests("simple_agent_without_streaming.txt") 
    logger = Logger(logger_file_path) 
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST") 
        llm_data_loader = LLMDataLoader(model="gpt-3.5-turbo",api_key=key,llm_spec={"stream":True}) 
        llm_call = LLMCall(llm_data_loader=llm_data_loader, logger=logger) 
        simple_agent = SimpleAgent(llm_call=llm_call,logger=logger) 
        simple_agent.set_system_prompt("You are a helpful assistant, you respond in an concise way") 
        response = simple_agent("is it still woth it to invest time learning programming in the \
                     era of the AI") 



        if not isinstance(response,str) : 
            for chunk in response : 
                delta = getattr(chunk.choices[0].delta, 'content', None)
                if delta : 
                    print(delta,end="",flush=True)
        else : 
            raise ValueError("the response is not in the correct type")


    
    print("### end simple agent with streaming ###")