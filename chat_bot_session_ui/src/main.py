from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from models import GPTCall, StreamHandler
from chat_bot_session_ui.src.utils import load_env
from langchain.schema import HumanMessage
import asyncio
import os 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stream_handler = StreamHandler() 
with load_env(["OPENAI_API_KEY"]) : 
    key = os.environ.get("OPENAI_API_KEY") 
    gpt_call = GPTCall(
        model = "gpt-4", 
        call_back_handler = stream_handler, 
        api_key = key
    )

@app.get("/chat",response_class=HTMLResponse) 
def get_table_page() : 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Move up one directory to root, then into 'templates'
    root_dir = os.path.dirname(base_dir)
    html_path = os.path.join(root_dir, "templates", "chatbot.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()

@app.get("/tests",response_class=HTMLResponse)
def get_chat_page() : 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    html_path = os.path.join(root_dir, "templates", "table.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()

@app.get("/agent_config",response_class=HTMLResponse)
def get_config_page() : 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    html_path = os.path.join(root_dir, "templates", "agent_config.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()

@app.get("/response") 
async def llm_response(prompt:str) : 
    print("user query",prompt)
    async def token_generator() : 
        async for chunk in gpt_call(HumanMessage(content=prompt)): 
            token = chunk.content
            yield token 
            await asyncio.sleep(0)
            print(token,end="")
        yield "\n [DONE]"

    return StreamingResponse(token_generator(),media_type="text/plain")
