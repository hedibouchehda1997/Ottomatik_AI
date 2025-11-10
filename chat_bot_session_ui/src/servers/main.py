from fastapi import FastAPI, Request 
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
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient, errors
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
tools_loader.set_tools([TavilySearchTool]) 


session_manager = SessionManager(user_id="123")

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    
    # The ping command is cheap and confirms connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
    
except errors.ServerSelectionTimeoutError as err:
    print("Could not connect to MongoDB:", err)



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


class TestSet(BaseModel) : 
    Cols : List[str] 
    metrics : Dict

class TestRow(BaseModel) : 
    tests : List[Dict]

class TestFullTable(BaseModel) : 
    table_name : str 
    tests : List[Dict]



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
    print("the type of created agent") 
    print(type(session_manager.agent))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "chatbot.html")
    print(html_path)
    return templates.TemplateResponse("chatbot.html", {"request":request,"data": agent_details})
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
    data_2_send = {
        "user" : "John Doe", 
        "age" : 30 , 
        "skills" : "python"
    }
    agent_details = agent_factory.get_agent_details()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "agent_config.html")
    return templates.TemplateResponse("agent_config.html", {"request":request,"data": agent_details})

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

    

@app.post("/set_agent") 
async def set_agent(request:Request,
                    agent_details:ReactDetails|ToolCallingDetails|ChatBotDetails) : 
    print("setting agent endpoint") ; 
    print(f"agent_details") 
    print(agent_details.dict())
    agent_factory.set_agent_details(agent_details.dict())
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

@app.get("/response") 
async def llm_response(prompt:str) : 
    print("last streamed response ")
    session_manager.agent.simple_memory.dump()
    async def token_generator() : 
        session_manager.last_streamed_response= ""
        for chunk in session_manager.agent(prompt): 
            delta = getattr(chunk.choices[0].delta, 'content', None)
            if delta : 
                session_manager.last_streamed_response += delta
                yield delta 
        session_manager.agent.add_query_response(user_query=prompt, 
                                                 ai_response=session_manager.last_streamed_response)
        yield "\n [DONE]"

    print("\n\n\n\n\n")


    return StreamingResponse(token_generator(),media_type="text/plain")