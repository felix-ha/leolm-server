import os
from pathlib import Path
import time
import requests
import tempfile
import streamlit as st
from index import get_wiki_article
from config import configuration
from model_api import LLMResponse, LLMResponseCreate


ip_adress_server = os.getenv('IP_ADRESS_SERVER', 'localhost')
url_server = f'http://{ip_adress_server}:{configuration.server.port}'


def server_is_online(url_server: str, route_status:str) -> bool:
    try:
      response = requests.get(f'{url_server}{route_status}')
      print(response)
      if response.status_code == 200:
        return True
      else:
        return False
    except requests.exceptions.ConnectionError:
      return False


def ask_model(url_server: str, route_status:str, route_model: str, question: str, context: str, prompt_history: str = None, path_to_upload=None) -> LLMResponse:
    if server_is_online(url_server, route_status):
        payload = {'question': question, 'prompt_history': prompt_history}
        respone = response = requests.post(f'{url_server}{route_model}', data=payload)
        if response.status_code == 200:
            return LLMResponse.model_validate(response.json())
        return LLMResponse(answer="No transformer is online.")

    #     payload = {'question': question, 'context': context, 'prompt': prompt_history}

    #     # Send file only at start of conversation
    #     if path_to_upload and prompt_history is None:
    #         prompt_history = None
    #         with open(path_to_upload, "rb") as f:
    #             file = {'file': f}
    #             response = requests.post(f'{url_server}{route_model}', files=file, data=payload)
    #             response = response.json()[0]
    #     else:
    #         response = requests.post(f'{url_server}{route_model}', data=payload)
    #         response = response.json()[0]

    #     prompt_history = response['answer'][0]['generated_text']
    #     answer = prompt_history.split('<|im_start|>assistant')[-1].lstrip()
    #     return answer, prompt_history, response['context']
    # else:
    #     return "LLM ist offline!", None, None



with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    context = None
    path_to_upload = None

    st.write("""
    # Frag  LeoLM!
    """)

    # advanced = st.toggle('Erweiterte Einstellungen')

    # if advanced:
    #     chunk_size = st.slider('chunk_size', 10, 10_000, value=100, step=50, help="Länge der Textabschnitte, die in die Vektordatenbank geladen werden.")
    #     chunk_overlap = st.slider('chunk_overlap', 0, 500, value=10, step=10, help="Überlappung der Textabschnitte, die in die Vektordatenbank geladen werden.")
    #     n_results = st.slider('n_results', 1, 10, value=3, step=1, help="Anzahl der Ergebnisse, die zurückgegeben werden und als Kontext verwendet werden.")

    # option = st.selectbox(
    # 'Was möchtest du fragen?',
    # ('Freie Frage', 'Frage Wikipedia', 'Frage zu einem Dokument'))

    # if option == 'Frage zu einem Dokument':
    #     files = st.file_uploader("File upload", type=["txt"], accept_multiple_files=True)

    #     if len(files) == 0:
    #         st.info("Keine Datei ausgewählt.")

    #     if len(files) >= 1:
    #         for i in range(len(files)):
    #             path_to_upload = tmpdir_path / files[i].name

    #             bytes_data = files[i].read() 
    #             with open(path_to_upload, "wb") as f:
    #                 f.write(bytes_data) 

    #             # TODO: Accept multiple files
    #             break
            
    #         if len(files) > 1:
    #             st.warning("Nur eine Datei ist akutell unterstützt! Jede weitere Datei wird ignoriert.")

    # elif option == 'Frage Wikipedia':
    #     wiki_keyword = st.text_input('Artikel', help='Der Wikipedia Artikel, welcher am besten zum Stichwort passt, wird ausgewählt')

    #     if wiki_keyword:
    #         wiki_article = get_wiki_article(wiki_keyword)
    #         st.write(f"Wikipedia Artikel - {wiki_article.original_title} - wird befragt.")

    #         path_to_upload = tmpdir_path / "wikipedia.txt"

    #         with open(path_to_upload, "w", encoding="utf-8") as f:
    #             f.write(wiki_article.content)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Eingabe..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            prompt_history = None
            if len(st.session_state.messages) > 2:
                prompt_history = st.session_state.messages[-2]['prompt_history']
                path_to_upload = None
            print(prompt_history)
            llm_result = ask_model(url_server, configuration.server.routes.status, configuration.server.routes.model, prompt, context, prompt_history, path_to_upload)
            print(llm_result)
            for chunk in llm_result.answer.split():
                full_response += chunk + " "
                time.sleep(0.1)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response, "prompt_history": llm_result.prompt_history, "context": context})

        if context:
            st.write(f'Beantwortet mit Kontext:\n {st.session_state.messages[-1]["context"]}')
