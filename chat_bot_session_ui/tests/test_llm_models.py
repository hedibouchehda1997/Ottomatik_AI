from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader, LLMCall
from chat_bot_session_ui.src.models.openai_models import GPTCall
from chat_bot_session_ui.src.utils.custom_logger import Logger
from chat_bot_session_ui.src.utils.env_utils import load_env
from chat_bot_session_ui.src.utils.tests_utils import create_txt_file_in_tests
import os


def test_standard_gpt_call() : 
    print("### start standart gpt call test ###")
    logger_file_path = create_txt_file_in_tests("stard_gpt_call_test_logger.txt")
    logger = Logger(logger_file_path) 
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST") 
        print("printing the key") 
        llm_data_loader = LLMDataLoader(model="gpt-3.5-turbo",api_key=key,llm_spec={})
        llm_call = LLMCall(llm_data_loader=llm_data_loader,logger=logger)
        messages = [{"role":"user","content":"tell me three jokes"}]
        response = llm_call(messages)
        print(response)
        print(type(response))
        assert(response,str)


    logger.build_logging_page()
    
    
    print("### end standart gpt call test ###")
