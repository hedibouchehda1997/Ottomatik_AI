import streamlit as st 
import random 
import time 
from typing import Dict, List
from streamlit.delta_generator import DeltaGenerator

class ChatBotGui : 
    def __init__(self, title: str, container: DeltaGenerator, history: List[Dict[str, str]] = []) : 
        # Inputs : 
        #   title : Mandatory, title of the chatbot 
        #   container : Mandatory, where the container will be placed in the page
        #   history : optional, previous conversation loaded from memory 
        self.number = 0 
        self.title = title 
        self.container = container
        
        self.history = history 
        if "messages" not in st.session_state: 
            st.session_state.messages = history 
        if "last_validated" not in st.session_state:
            st.session_state.last_validated = True # Initially True, so user can start chatting

    def validatade_tool(self):
        print("validate !!")
        st.success("validate !!")
        # Allow user to send a new message after validation
        st.session_state.last_validated = True

    def render(self):
        with self.container: 
            st.title(self.title)
            # Scrollable messages container
            messages_container = st.container()
            last_msg_idx = len(st.session_state.messages) - 1
            for idx, message in enumerate(st.session_state.messages):
                with messages_container:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                        # Only add a Validate button to assistant messages that are the last one
                        if (
                            message["role"] == "assistant"
                            and idx == last_msg_idx
                            and not st.session_state.last_validated
                        ):
                            if st.button("Validate", key=f"validate_{idx}"):
                                self.validatade_tool()
            
            # Accept user input (always at the bottom)
            # Only allow input if last response is validated

            # Input field is disabled when waiting for validation
            can_send_message = st.session_state.last_validated

            print("can_send_message : ",can_send_message)
            prompt = st.chat_input(
                "Say something...", 
                disabled=not can_send_message
            )

            
            if prompt and can_send_message:
                with messages_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    st.session_state.messages.append({"role": "user", "content": prompt})

                    response = f"Echo: {prompt}  \n\n"
                    with st.chat_message("assistant"):
                        st.markdown(response)
                        # Add Validate button for new response, using unique key
                        # Disable future input until validation
                        st.session_state.last_validated = False
                        if st.button("Validate", key=f"validate_{len(st.session_state.messages)}"):
                            self.validatade_tool()
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__" : 

    st.set_page_config(layout="wide")

    # 💡 Add CSS to make both columns stretch to equal height
    st.markdown("""
    <style>
    .block-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    .stHorizontalBlock {
        display: flex;
        align-items: stretch;
    }
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1]) 

    with col1:
        chat_container = st.container() 
        chat_ui = ChatBotGui(title="Simple Chat", container=chat_container)
        chat_ui.render() 

    with col2: 
        st.subheader("Agent Configuration")
        # Make agent_type selection outside the form, then show the rest
        agent_type = st.selectbox(
            "Agent type",
            ["ReAct", "Plan and Execute", "Tool calling", "Self Reflection"],
            key="agent_type_select"
        )

        # Show text input ONLY when Tool calling is selected
        text_input_value = None
        if agent_type == "Tool calling":
            text_input_value = st.text_input(
                "Text",
                key="tool_calling_text"
                # Value is updated directly in session_state
            )
        else:
            # Optional: clear the tool_calling_text in session_state when another agent type chosen
            st.session_state.pop("tool_calling_text", None)
            st.session_state.pop("tool_calling_text_callback_message", None)
        
        model_choice = st.selectbox(
            "Model",
            ["gpt-4", "gpt-3.5-turbo"]
        )

        apply_clicked = st.button("Apply", key="apply_agent_config_button")

        if apply_clicked:
            # Optional callback-like processing can happen after Apply
            if agent_type == "Tool calling":
                st.session_state["tool_calling_text_callback_message"] = f"Input now: {st.session_state.get('tool_calling_text', '')}"
            else:
                st.session_state.pop("tool_calling_text_callback_message", None)
            print("zebi")
            st.success(f"Settings applied: Agent={agent_type}, Model={model_choice}")
            # Show info message, if any
            if st.session_state.get("tool_calling_text_callback_message"):
                st.info(st.session_state["tool_calling_text_callback_message"])
        else:
            # Show info message if present and apply not pressed
            if st.session_state.get("tool_calling_text_callback_message"):
                st.info(st.session_state["tool_calling_text_callback_message"])
        # Chat interface (left) remains fully independent of the config (right)