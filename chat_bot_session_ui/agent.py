from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
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

    tavily_tool = Tool(
        name="TavilySearch",
        func=tavily_search,
        description="Searches the web using Tavily and returns relevant results."
    )

    # --- 2. Setup the chat model with streaming ---
    chat_model = ChatOpenAI(
        model_name="gpt-4",
        openai_api_key=key,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )

    # --- 3. Initialize the agent ---
    agent = initialize_agent(
        tools=[tavily_tool],
        llm=chat_model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # --- 4. Run the agent ---
    query = "Latest news on AI advancements"
    print("testtst   \n\n **************")
    for output in agent.stream(query) : 
        print("s\n")
        print(output,end="")
    # agent.run(query)