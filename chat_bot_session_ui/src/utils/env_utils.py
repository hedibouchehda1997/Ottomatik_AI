from dotenv import load_dotenv, find_dotenv
from typing import List, Dict, Tuple 
from contextlib import contextmanager
import csv 
import os 


@contextmanager
def load_env(api_keys_list:List[str]) : 
    path = find_dotenv()
    load_dotenv("chat_bot_session_ui\.env") 
    try : 
        yield 
    finally : 
        for api_key in api_keys_list : 
                os.environ.pop(api_key,None)