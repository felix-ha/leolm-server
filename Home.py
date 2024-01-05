import streamlit as st

st.set_page_config(
    page_title="transformers-playground",
    page_icon=None,
)

st.write("# transformers playground!")

st.markdown(
    """
    ## Chat CPU
    This uses a [ollama](https://github.com/jmorganca/ollama) as a backend and is usually online but is very slow.
    ## Chat GPU and Ask a Dokument
    This uses a custom server that runs on a paperspace vm and is usually offline.
    ### Implemented models:
    - [LeoLM](https://huggingface.co/LeoLM/leo-mistral-hessianai-7b-chat)
"""
)
