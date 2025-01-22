"""
This file is "My Chat Bot" app page.
"""

import streamlit as st

from common.chat import Chat


chat = Chat()

if "chat" not in st.session_state:
    st.session_state.chat = Chat()

for content in st.session_state.chat.history:
    if content["role"] != "system":
        with st.chat_message(content["role"]):
            st.markdown(content["content"])

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.session_state.chat.discuss(prompt)
        st.markdown(response)
