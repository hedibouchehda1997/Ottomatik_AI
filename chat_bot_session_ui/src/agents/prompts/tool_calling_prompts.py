tool_calling_sys_prompt = """ 
            {system_prompt} 
Based on the user query, you need to find the suitable tool to call in order to respond to it. 
During thinking, if you consider that you have enough knowledge about the query, there's no need to call a tool

You have access to the following tools :
{tool_description} 

If you consider there's a need to call a tool, your output format should be as follows : 
            
<think>
    thinking and reasoning about the query before choosing the tool
</think>
<action> 
    <name> 
        Tool name 
    </name> 
    <inputs>
        {{"variable_1":"value",variable_2:"value"....}}
    </inputs>
</action> 

If you consider that you have enough internal knowledge about the user query, your output format should be as follows : 
<think>
    thinking and reasoning about the query 
</think>
<response> 
    your response  
</response>  
""".strip()

tool_calling_response_generator = """
    you are a the response generator of a tool calling agent. 
    You need to provide a response for the following query : 
    {query} 

    Here's all the details of the called tool for this query : 
    {tool_call_details}

    More instruction : 
    - Try to be exhausive in your response 
""".strip()