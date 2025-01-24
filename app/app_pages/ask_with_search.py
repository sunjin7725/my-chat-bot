"""
This module provides the Streamlit page for asking questions based on search results.

It allows users to input questions and receive answers generated from the search results
using the chat_with_search function.
"""

import streamlit as st

from common.ask_with_search import chat_with_search
from common.streamlit_utils import display_chat_history, talk

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

display_chat_history(st.session_state.chat_history)

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    with st.chat_message("user"):
        talk(prompt, "user", st.session_state.chat_history)
    with st.chat_message("assistant"):
        response = chat_with_search(prompt, st.session_state.chat_history)
        talk(response, "assistant", st.session_state.chat_history)
