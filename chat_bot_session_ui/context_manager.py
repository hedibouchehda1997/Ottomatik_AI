from contextlib import contextmanager
from dotenv import load_dotenv, find_dotenv
from typing import List
import os

@contextmanager 
def load_env(api_keys_list:List[str]) : 
    path = find_dotenv()
    load_dotenv(path) 
    try : 
        yield 
    finally : 
        for api_key in api_keys_list : 
            os.environ.pop(api_key,None)