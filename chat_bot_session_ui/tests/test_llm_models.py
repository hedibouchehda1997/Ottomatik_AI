from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader
from chat_bot_session_ui.src.models.openai_models import GPTCall
from chat_bot_session_ui.src.utils.custom_logger import Logger


def test_standard_gpt_call() : 
    print("### start standart gpt call test ###")
    logger = Logger("test_logger.txt") 
    # llm_data_loader = LLMDataLoader()
    
    
    print("### end standart gpt call test ###")
