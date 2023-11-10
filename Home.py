import streamlit as st

st.set_page_config(
    page_title="transformers-playground",
    page_icon=None,
)

st.write("# transformers playground!")

st.markdown(
    """
    ### Implemented models:
    - [LeoLM](https://huggingface.co/LeoLM/leo-mistral-hessianai-7b-chat)
"""
)