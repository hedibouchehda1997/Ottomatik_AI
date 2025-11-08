from typing import Any 
from tavily import TavilyClient 
from .tools import Tool 

def tavily_search(query:str, engine:str="google", location : str="", top_n : int=10) -> Any: 

    # Initialize the client with your API key
    client = TavilyClient(api_key="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")

    # Perform a search
    response = client.search(
        query=query,
        search_depth="basic",     # or "advanced"
        max_results=1              # number of results to retrieve
    )

    output = ""
    # Print results
    for result in response.get("results", []):

        output += f"Title : {result.get('title')}\n" 
        output += f"URL: {result.get('url')}\n" 
        output += f"Snippet: {result.get('content')}\n\n"
    
    return output 



TavilySearchTool = Tool(
    name = "tavily_search" , 
    exterior_name = "Tavily Search" , 
    description = """
This tool allow doing web search on google. 
Inputs : 
    query : "the query to search on google" 
output : 
    Title of the found web page 
    its url 
    a snippet of it content     
""",
    func = tavily_search
)