from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from chat_bot_session_ui.src.utils.tools_loader import ToolsLoader
from chat_bot_session_ui.src.tools.web_search_tools import TavilySearchTool
from typing import Dict, List
from pydantic import BaseModel



app = FastAPI() 
tools_loader = ToolsLoader() 
tools_loader.add_tool(TavilySearchTool)


class ToolDetails(BaseModel) : 
    name : str 
    inputs : Dict


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run_tool") 
def run_tool(tool_details : ToolDetails) : 
    print(f"tool details from the server : \n {tool_details.dict()}")
    response = tools_loader.run_tool(tool_details.dict())  
    
    return {"response":response}