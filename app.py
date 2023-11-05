import streamlit as st

st.set_page_config(
    page_title="LLM Server",
    page_icon=None,
)

st.write("# Welcome to the LLM Server")

st.sidebar.success("Choose a model.")

st.markdown(
    """
    A app to test llms.

    ### Implemented models:
    - [LeoLM](https://huggingface.co/LeoLM/leo-mistral-hessianai-7b-chat)
    - [BLIP-2](https://huggingface.co/Salesforce/blip2-opt-2.7b)
"""
)