import streamlit as st
from dataclasses import dataclass

from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings 
from llama_index.llms.gemini import Gemini 
Settings.llm = Gemini()
tool_spec = DuckDuckGoSearchToolSpec()

agent =ReActAgent.from_tools(tool_spec.to_tool_list())


@dataclass
class Message:
    actor: str
    payload: str


USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi!How can I help you?")]

msg: Message
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

prompt: str = st.chat_input("Enter a prompt here")

if prompt:
    prompt = prompt.replace('\n','\n\n')
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)
    response:str = agent.chat(prompt).response
    
    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
    st.chat_message(ASSISTANT).write(response) 



