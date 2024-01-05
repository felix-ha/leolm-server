import os
import httpx
import time
import streamlit as st
from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    role: str
    content: str


class Chat(BaseModel):
    messages: Optional[list[Message]] = []

    def add_question(self, question: str):
        self.messages.append(Message(role="user", content=question))

    def add_answer(self, answer: str):
        self.messages.append(Message(role="assistant", content=answer))


class LLMQuestion(BaseModel):
    question: str
    chat: Chat


class LLMResponse(BaseModel):
    answer: str
    chat: Chat

import logging
logging.basicConfig(level=logging.INFO)


def server_is_online(url_server: str, route_tags: str) -> bool:
    try:
        response = httpx.get(f"{url_server}{route_tags}", timeout=None)
        print(response)
        if response.status_code == 200:
            logging.info(f"Server is online.")
            return True
        else:
            logging.info(f"Server is offline.")
            return False
    except:
        logging.info(f"Server is offline.")
        return False


def get_available_models(url_server: str, route_tags: str) -> bool:
    response = httpx.get(f"{url_server}{route_tags}", timeout=None)
    if response.status_code == 200:
        data = response.json()
        models = [model['name'].split(':')[0] for model in data['models']]
        logging.info(f"Available models: {models}")
        return models
    else:
        return []


def pull_model(url_server: str, route_pull: str, model: str) -> bool:
    data = {"name": model}
    response = httpx.post(f"{url_server}{route_pull}", json=data, headers={"Content-Type": "application/json"})
    print(response)
    if response.status_code == 200:
        logging.info(f"Model {model} loaded.")
        logging.info(f"Output\n {response.text}")
    else:
        logging.info(f"Model {model} not loaded.")


ip_adress_server = os.getenv("IP_ADRESS_SERVER_CPU", "localhost")
port = 5001
url_server = f"http://{ip_adress_server}:{port}"
route_tags = "/api/tags"
route_pull = "/api/pull"
route_chat = "/api/chat"

MODEL = 'llama2-uncensored'

if "chat" not in st.session_state:
    st.session_state.chat = Chat()

st.write(
   f"""
# chat with a language model
runs on [ollama](https://github.com/jmorganca/ollama)
"""
)

MODEL = st.selectbox(
    'Choose model',
    ('llama2',
      'llama2-uncensored', 
      'phi',
      'mistral',
      'dolphin-phi',
      'neural-chat', 
      'starling-lm',
      'codellama', 
      'orca-mini', 
      'vicuna'), index = 2)


for message in st.session_state.chat.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

if question := st.chat_input("input..."):
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        st.session_state.chat.add_question(question)    

        if server_is_online(url_server, route_tags):
            models = get_available_models(url_server, route_tags)
            if MODEL not in models:
                logging.info(f"Model {MODEL} not available.")
                pull_model(url_server, route_pull, MODEL)

        messages = st.session_state.chat.model_dump()
        data = {"model": MODEL, "stream": False}
        data.update(messages)
        
        try:
            response = httpx.post(f"{url_server}{route_chat}", json=data, headers={"Content-Type": "application/json"}, timeout=None)
            if response.status_code == 200:
                json_response = response.json()
                answer = json_response['message']['content']
            else:
                answer = "No transformer is online."
        except:
            logging.exception(f"Server is offline.")
            answer = "No transformer is online."

        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.1)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        st.session_state.chat.add_answer(answer)

