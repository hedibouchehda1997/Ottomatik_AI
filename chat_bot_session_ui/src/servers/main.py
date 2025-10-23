from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .models import GPTCall
from .utils import load_env
import asyncio
import os 

app = FastAPI()
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(base_dir, "templates")
templates = Jinja2Templates(directory=templates_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with load_env(["OPENAI_API_KEY"]) : 
    key = os.environ.get("OPENAI_API_KEY") 
    gpt_call = GPTCall(
        model = "gpt-4", 
        system_prompt = "You are a helpful assistant", 
        api_key = key
    )

@app.get("/chat",response_class=HTMLResponse) 
def get_table_page(request : Request) : 
    data_2_send = {
        "user" : "John Doe", 
        "age" : 30 , 
        "skills" : "python"
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
    data_2_send = {
        "user" : "John Doe", 
        "age" : 30 , 
        "skills" : "python"
    }
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "table.html")
    return templates.TemplateResponse("table.html", {"request":request,"data": data_2_send})

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "agent_config.html")
    return templates.TemplateResponse("agent_config.html", {"request":request,"data": data_2_send})

    # if os.path.exists(html_path):
    #     with open(html_path, "r", encoding="utf-8") as f:
    #         return f.read()

@app.get("/response") 
async def llm_response(prompt:str) : 
    print("user query",prompt)
    async def token_generator() : 
        async for chunk in gpt_call(prompt): 
            token = chunk.content
            yield token 
            await asyncio.sleep(0)
            print(token,end="")
        yield "\n [DONE]"

    return StreamingResponse(token_generator(),media_type="text/plain")
