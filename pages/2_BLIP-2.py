import streamlit as st
import os
import requests


ip_adress_server = os.getenv('IP_ADRESS_SERVER', 'localhost')
port = 5000
url_server = f'http://{ip_adress_server}:{port}'
route_blip2 = '/blip2'

st.write("""
# BLIP-2
""")

if st.button('Ask model'):
    response = requests.post(f'{url_server}/{route_blip2}')
    response = response.json()
    st.write(response['answer'])
