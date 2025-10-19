from openai import OpenAI
import os
from contextlib import contextmanager
from dotenv import load_dotenv, find_dotenv
from context_manager import load_env

# --- 1. Define the Tavily search tool ---
def tavily_search(query: str) -> str:
    # This is a placeholder for your actual Tavily search API call
    # Replace it with real API logic
    return f"Results for '{query}' from Tavily"




with load_env(["OPENAI_API_KEY"]) :

    key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=key)

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "how to make a fuel without co2 write me 4 paragraph esssay about it !"}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)


