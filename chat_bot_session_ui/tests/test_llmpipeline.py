from chat_bot_session_ui.src.models import GPTCall 
from chat_bot_session_ui.src.context_manager import load_env
from chat_bot_session_ui.src.agent_loader import LLMPipelineSessionManager
from collections.abc import Generator
import uuid 
import os 


def test_streaming() : 
    print("#### start running streaming test ######") 
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST")
        gpt_call = GPTCall(
            model="gpt-3.5-turbo", 
            api_key = key , 
            system_prompt = "You are a helpful assistant", 
        )   
        response = gpt_call("Tell me for 4 jokes") 
        assert(isinstance(response,Generator))
        for token in response : 
            print(token,end="",flush=True)
    print("### end running streaming test")

def test_llm_pipeline_add_new_element() :
    print("### start running llm pipline test ###")
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST") 
        new_user_id = uuid.uuid4().hex 
        new_agent_id = uuid.uuid4().hex 
        agent_title = "Tool calling agent" 
        version = 0
        agent_details = {
            "agent_type" : "Tool calling" , 
            "model" : "gpt-3.5-turbo" , 
            "system_prompt" : "You are a helpful assistant", 
            "tools" : ["tavily_search"]
        }

        # Get absolute path to test agent database JSON file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "agent_database_test.json")

        llm_pipeline = LLMPipelineSessionManager(json_path)
        size_before_add = llm_pipeline.get_count_of_database()
        
        llm_pipeline.add_or_update_agent_version(
            agent_id = new_agent_id , 
            version = version , 
            agent_title = agent_title, 
            agent_details = agent_details ,
            user_id=new_user_id, 
        )

        llm_pipeline.save()
        size_after_add = llm_pipeline.get_count_of_database() 
        assert(size_after_add == size_before_add+1)
        print("### end running llm pipeline test")

def test_llm_pipeline_check_exsisting_element() : 
    print("### start running checking esisting element ###") 
    with load_env(["OPENAI_API_KEY_TEST"]) : 
        key = os.environ.get("OPENAI_API_KEY_TEST") 
        new_user_id = "1ef4fadb31ca4cc5b2619b5561ec13aa" 
        new_agent_id = "b540e8d32a654ff9a38be598b2a74858"
        agent_title = "Tool calling agent" 
        version = 0
        agent_details = {
            "agent_type" : "Tool calling" , 
            "model" : "gpt-3.5-turbo" , 
            "system_prompt" : "You are a helpful assistant", 
            "tools" : ["tavily_search"]
        }

        # Get absolute path to test agent database JSON file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "agent_database_test.json")

        llm_pipeline = LLMPipelineSessionManager(json_path)
        size_before_add = llm_pipeline.get_count_of_database()
        
        llm_pipeline.add_or_update_agent_version(
            agent_id = new_agent_id , 
            version = version , 
            agent_title = agent_title, 
            agent_details = agent_details ,
            user_id=new_user_id, 
        )

        size_after_add = llm_pipeline.get_count_of_database() 
        assert(size_after_add == size_before_add)

    print("### end running checking esisting element ###")

