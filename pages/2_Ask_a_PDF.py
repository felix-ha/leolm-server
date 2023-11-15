import os
from pathlib import Path
import time
import httpx
import tempfile
import streamlit as st
from config import configuration
from logic import LLMResponse, LLMQuestion, Chat


ip_adress_server = os.getenv("IP_ADRESS_SERVER", "localhost")
url_server = f"http://{ip_adress_server}:{configuration.server.port}"


def server_is_online(url_server: str, route_status: str) -> bool:
    try:
        response = httpx.get(f"{url_server}{route_status}", timeout=None)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def ask_model(
    url_server: str, route_status: str, route_model: str, route_upload: str, llm_question: LLMQuestion, file_to_upload: str
) -> LLMResponse:
    if server_is_online(url_server, route_status):
        if file_to_upload:
            # TODO open files with context manager
            files = [('files', open(file_to_upload, 'rb'))]
            response_upload = httpx.post(f"{url_server}{route_upload}", files=files, timeout=None)

        response = httpx.post(
            f"{url_server}{route_model}", json=llm_question.model_dump(), timeout=None
        )
        if response.status_code == 200:
            return LLMResponse.model_validate(response.json())
        else:
            return LLMResponse(answer="No transformer is online.", chat=Chat())
    else:
        return LLMResponse(answer="No transformer is online.", chat=Chat())


with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)

    if "chat" not in st.session_state:
        st.session_state.chat = Chat()
    if "file_was_uploaded" not in st.session_state:
        st.session_state.file_was_uploaded = False

    st.write(
        """
    # chat with a transformer
    """
    )


    file_to_upload = None
    file = st.file_uploader("File upload", type=["pdf"], accept_multiple_files=False)

    if file:
        file_to_upload = tmpdir_path / file.name

        bytes_data = file.read() 
        with open(file_to_upload, "wb") as f:
            f.write(bytes_data) 


    for message in st.session_state.chat.messages:
        with st.chat_message(message.role):
            st.markdown(message.content)

    if question := st.chat_input("input..."):
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            llm_question = LLMQuestion(question=question, chat=st.session_state.chat)

            if st.session_state.file_was_uploaded:
                file_to_upload = None

            llm_result = ask_model(
                url_server,
                configuration.server.routes.status,
                configuration.server.routes.model,
                configuration.server.routes.upload,
                llm_question,
                file_to_upload
            )
            for chunk in llm_result.answer.split():
                full_response += chunk + " "
                time.sleep(0.1)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.chat.add_question(llm_question.question)
        st.session_state.chat.add_answer(llm_result.answer)

        st.session_state.file_was_uploaded = True
