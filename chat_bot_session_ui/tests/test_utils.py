from chat_bot_session_ui.src.models import GPTCall 
from chat_bot_session_ui.src.utils import load_env, Data, DataLoader, CSVHandler, create_csv_in_tests
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

def test_llm_pipeline_sessions_manager_add_new_element() :
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

def test_llm_pipeline_sessions_manager_check_exsisting_element() : 
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

def test_DataLoader_and_CSVHandler() : 
    print("### strart running DataLoader and CSVHandler objects") 
    cols =  [{"key":"col1","label":"User query","widthWeight":1},{"key":"col2","label":"Ground truth","widthWeight":1}] 
    query_ref_pairs = [
        {"col1":"""Why does salt melt ice on the road during winter?""","col2":"""Salt lowers the freezing point of water, a process known as freezing point depression. When salt is added to ice, it dissolves into the thin layer of liquid water always present on the ice surface, forming a brine with a lower freezing point than pure water. As a result, the ice melts even though the temperature is below 0°C."""} ,
        {"col1":"""What is wrong with this Python code and how can I fix it?

my_list = [1, 2, 3]
print(my_list[3]) ""","col2":"""The code raises an IndexError because list indices in Python start at 0, so my_list[3] is out of range. The valid indices are 0, 1, 2.
✅ Fix:

print(my_list[2])


or

for item in my_list:
    print(item)""",
        },
        {"col1" :  """Summarize this text in one sentence:
“Artificial intelligence refers to systems that can perform tasks that typically require human intelligence, such as understanding language, recognizing patterns, solving problems, and learning from experience.” """,
    "col2":"""Artificial intelligence is the development of systems capable of performing human-like cognitive tasks such as learning, problem-solving, and language understanding."""},
        {"col1":"""Explain the difference between supervised and unsupervised learning in machine learning. """, 
    "col2":"""In supervised learning, models are trained on labeled data — each input has a known output (e.g., classifying emails as spam or not spam).
In unsupervised learning, models are trained on unlabeled data and must discover hidden structures or patterns by themselves (e.g., clustering customers by purchasing behavior). """}, 
        {"col1":"""Write a short motivational quote about learning to code.""",
    "col2":"""Every bug you fix is a lesson learned; every line of code is a step toward mastery."""}
    ]

    # data_loader = DataLoader(data=data,metrics=metrics)
    # print("columns : ") 
    # print(data_loader.columns)
    # print("first row")
    file_path = create_csv_in_tests("csv_test.csv")
    csv_handler = CSVHandler(file_path) 
    csv_handler.set_data_and_cols(cols,query_ref_pairs)
    csv_handler.write_table_to_csv()
    cols, data = csv_handler.load_table_from_csv() 

    data = Data(columns=cols,data=data)
    metrics = [{"label":"output","widthWeight":1},{"label":"relevance","widthWeight":1}]
    data_loader = DataLoader(csv_handler=csv_handler,metrics=metrics)
    # print("##### \n##### \n######")
    # print("printing cols" )
    # for col in cols : 
    #     print(col) 

    print("### end running DataLoader and CSVHandler objects") 



