import streamlit as st 
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler 
from langchain.schema import SystemMessage,HumanMessage
from context_manager import load_env 
import os

class StreamHandler(BaseCallbackHandler) : 
    def __init__(self) : 
        self.text = ""

    def on_llm_new_token(self,token:str,**kwargs) : 
        self.text += token 
        # self.placeholder.(self.text)

class GPTCall : 
    def __init__(self,model:str,call_back_handler:StreamHandler,api_key:str,system_prompt:SystemMessage=None) : 
        self.model = model 
        self.call_back_handler = call_back_handler 
        self.api_key = api_key 
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
                model = self.model, 
                streaming = True, 
                openai_api_key = api_key, 
                callbacks = [self.call_back_handler]
        )
    def __call__(self,human_message:HumanMessage) :
        messages = [human_message] 
        if self.system_prompt is not None : 
            messages.append(self.system_prompt)
        return self.llm.astream(messages) 


if __name__ == "__main__" : 
    st.title("streamed ChatOpenAI Response") 

    prompt = st.text_input("Enter your prompt : ")

    placeholder = "" 

    handler = StreamHandler(placeholder) 
    with load_env(["OPENAI_API_KEY"]) :

        key = os.environ.get("OPENAI_API_KEY")
        gpt_call = GPTCall(
                model = "gpt-4" ,
                call_back_handler = handler, 
                api_key = key, 
        )
        response = gpt_call(HumanMessage(content=prompt))
        print("printing response : ")
        print(response)

