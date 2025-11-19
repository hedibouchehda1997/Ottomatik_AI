from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from chat_bot_session_ui.src.agents.prompts.react_prompts import react_prompt
from chat_bot_session_ui.src.agents.prompts.tool_calling_prompts import tool_calling_sys_prompt,tool_calling_response_generator 
from chat_bot_session_ui.src.models.llm_models import TokenCounter, LLMDataLoader, LLMCall
from chat_bot_session_ui.src.utils.env_utils import load_env
from chat_bot_session_ui.src.utils.tools_loader import ToolsLoader
from chat_bot_session_ui.src.utils.agent_factory import AgentFactory
from chat_bot_session_ui.src.tools.web_search_tools import TavilySearchTool
from chat_bot_session_ui.src.utils.test_set_handler import TestSetHandler
from chat_bot_session_ui.src.utils.session_manager import SessionManager
from chat_bot_session_ui.src.utils.mongoDB_interactions import MongoDBInteractor
from fastapi.staticfiles import StaticFiles
import uuid 
import asyncio
import os 
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("base_dir") 
print(base_dir)
static_path = os.path.join(base_dir, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates_path = os.path.join(base_dir, "templates")
templates = Jinja2Templates(directory=templates_path)
tools_loader = ToolsLoader() 
tools_loader.add_tool(TavilySearchTool) 


session_manager = SessionManager(user_id="123")

mong_db_client = MongoDBInteractor("mongodb://localhost:27017/")


agent_factory = AgentFactory()
test_sets = []

tools_description_list = tools_loader.get_tools_description()  
for tool_description in tools_description_list : 
    print(f"tool_description : {tool_description}") 


class ReactDetails(BaseModel) : 
    agent_type : str 
    agent_name : str 
    count : int 
    model : str 
    system_prompt : str
    tools : List[str]


class ToolCallingDetails(BaseModel) : 
    agent_type : str 
    agent_name : str
    instruction_for_response_generator : str 
    model : str 
    system_prompt : str 
    tools : List[str] 

class ChatBotDetails(BaseModel) :
    agent_type : str 
    agent_name : str 
    model : str 
    system_prompt : str
    description : str
    id_ : str 
    version : int



class TestSet(BaseModel) : 
    Cols : List[str] 
    metrics : Dict

class TestRow(BaseModel) : 
    tests : List[Dict]

class TestFullTable(BaseModel) : 
    table_name : str 
    tests : List[Dict]

class ToolCallFinal(BaseModel) : 
    user_query : str 
    tool_call_result : str



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/chat",response_class=HTMLResponse) 
def get_table_page(request : Request) : 
    agent_details = agent_factory.get_agent_details()
    print("from chat endpoint ") 
    print(agent_details)
    # print("the type of created agent") 
    # print(type(session_manager.agent))
    memory = mong_db_client.get_memory(id_=agent_details["id_"])
    print(f"printing memeory from chat endpoint : \n {memory}")
    data_2_send = {
        "agents" : agent_details , 
        "memory" : memory["history"] 
    }
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "chatbot.html")
    print(html_path)
    return templates.TemplateResponse("chatbot.html", {"request":request,"data": data_2_send})
    # if os.path.exists(html_path):
    #     with open(html_path, "r", encoding="utf-8") as f:
    #         return f.read()

@app.get("/tests",response_class=HTMLResponse)
def get_chat_page(request : Request) : 
    agent_details = agent_factory.get_agent_details() 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "table.html")
    return templates.TemplateResponse("table.html", {"request":request,"data": agent_details})

    # if os.path.exists(html_path):
    #     with open(html_path, "r", encoding="utf-8") as f:
    #         return f.read()

@app.get("/agent_config",response_class=HTMLResponse)
def get_config_page(request : Request) : 
    
    versionning_form_data = {
        "patterns" : {
            "react" :{
                "prompt": react_prompt ,
                "text" : "React"  
                } , 
            "tool_calling" : {
                "text" : "Tool Calling" , 
                "prompts" : {
                    "prompt_tool_call":tool_calling_sys_prompt , 
                    "prompt_generator" : tool_calling_response_generator
                    }
                }, 
            "chat_bot" : {
                "text" : "Simple ChatBot"
            }
        }, 
        "tools" : tools_description_list , 
        "models" : ["gpt-3.5-turbo","gpt-4"]
    }
    agent_details = agent_factory.get_agent_details()

    data_2_send = {
        "agent_details" : agent_details , 
        "versionning_form_data" : versionning_form_data
    }
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "agent_config.html")
    return templates.TemplateResponse("agent_config.html", {"request":request,"data": data_2_send})

@app.get("/new_agent",response_class=HTMLResponse) 
def get_new_agent_config_page(request : Request) : 
    data_2_send = {
        "patterns" : {
            "react" :{
                "prompt": react_prompt ,
                "text" : "React"  
                } , 
            "tool_calling" : {
                "text" : "Tool Calling" , 
                "prompts" : {
                    "prompt_tool_call":tool_calling_sys_prompt , 
                    "prompt_generator" : tool_calling_response_generator
                    }
                }, 
            "chat_bot" : {
                "text" : "Simple ChatBot"
            }
        }, 
        "tools" : tools_description_list , 
        "models" : ["gpt-3.5-turbo","gpt-4"]
    }
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "single_agent_form.html") 
    print(f"html path : {html_path}")

    return templates.TemplateResponse("single_agent_form.html",{"request":request, "data":data_2_send})

    

@app.get("/agents_list",response_class=HTMLResponse)
async def get_agents_list(request: Request) : 
    agent_collection = mong_db_client.find_all_agents()
    print("agent collection ") 
    print(agent_collection)
    data_tst = {
        "agent_collection" : agent_collection
    }
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "agent_list.html")
    return templates.TemplateResponse("agent_list.html", {"request":request,"data": data_tst})


@app.post("/launch_agent") 
async def launch_agent(request:Request,
                        agent_details:ReactDetails|ToolCallingDetails|ChatBotDetails) : 
    agent_details_dict = agent_details.dict() 
    agent_factory.set_agent_details(agent_details_dict) 
    agent = agent_factory.build_agent() 
    session_manager.set_agent(agent)
    return {"response":"ok"}

@app.post("/set_agent") 
async def set_agent(request:Request,
                    agent_details:ReactDetails|ToolCallingDetails|ChatBotDetails, 
                    back_ground_taks : BackgroundTasks) : 
    print("setting agent endpoint") ; 
    print(f"agent_details") 
    agent_details_dict = agent_details.dict()
    print(f"printing agent details : \n {agent_details_dict}")
    agent_details_for_collection = agent_details_dict 
    agent_details_for_collection["version"] = 0 
    agent_details_for_collection["id_"] = str(uuid.uuid4()) 
    back_ground_taks.add_task(mong_db_client.add_agent,agent_details_dict)
    # print(agent_details_dict["instruction_for_response_generator"])
    agent_factory.set_agent_details(agent_details_for_collection)
    agent = agent_factory.build_agent()

    session_manager.set_agent(agent)
    return {"response":'ok'}


@app.post("/run_tests") 
async def run_tests(request:Request, 
                    tests_2_run :TestRow | TestFullTable ) : 
    print("run tests endpoint is working correctly")  
    print(f"type of input {type(tests_2_run)}")
    return {"response":"ok"}


@app.post("/new_test_table") 
async def build_new_test_set(request : Request, 
                            test_set_data : TestSet) : 
    test_sets.append(TestSetHandler(test_set_data.dict()))
    return {"response":"ok"}

@app.post("/final_response") 
async def get_tool_response(tool_call_final : ToolCallFinal) : 
    # print(f"tool call final : \n {tool_call_final.dict()}")
    print("from final_response endpoint ")
    print(tool_call_final.user_query)
    print(tool_call_final.tool_call_result)
    async def token_generator() : 
        for chunk in session_manager.agent.response_generator(tool_call_final.user_query, tool_call_final.tool_call_result ) :
            delta =  getattr(chunk.choices[0].delta, 'content', None)  
            if delta : 
                yield delta 

    

    return StreamingResponse(token_generator(),media_type="text/plain") 

@app.get("/response") 
async def llm_response(prompt:str) : 
    print("last streamed response ")
    agent_details = agent_factory.get_agent_details() 
    mong_db_client.add_message(id_=agent_details["id_"],type_="user",msg=prompt)
    if agent_details["agent_type"] == "chat_bot" : 
        session_manager.agent.simple_memory.dump()
    async def token_generator() : 
        if agent_details["agent_type"] == "chat_bot" : 
            session_manager.last_streamed_response= ""
            for chunk in session_manager.agent(prompt): 
                delta = getattr(chunk.choices[0].delta, 'content', None)
                if delta : 
                    session_manager.last_streamed_response += delta
                    yield delta 
            session_manager.agent.add_query_response(user_query=prompt, 
                                                 ai_response=session_manager.last_streamed_response)
            yield "\n [DONE]"
        elif agent_details["agent_type"] == "tool_calling" : 
            for chunk in session_manager.agent(prompt) : 
                yield chunk
        mong_db_client.add_message(id_=agent_details["id_"],type_="ai",msg=session_manager.last_streamed_response)
        

    print("\n\n\n\n\n")


    return StreamingResponse(token_generator(),media_type="text/plain") 