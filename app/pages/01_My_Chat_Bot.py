"""
This file is "My Chat Bot" app page.
"""

import streamlit as st

from utils.chat import Chat

if __name__ == "__main__":
    chat = Chat()

    TITLE = "My Chat Bot"
    st.set_page_config(page_title=TITLE, page_icon="🦑")

    st.markdown(f"# {TITLE}")

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
        with st.chat_message("assistant", avatar="🤖"):
            response = st.session_state.chat.discuss(prompt)
            st.markdown(response)
