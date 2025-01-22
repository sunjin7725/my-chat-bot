import streamlit as st

from common.ask_with_search import chat_with_search

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for content in st.session_state.chat_history:
    with st.chat_message(content["role"]):
        st.markdown(content["content"])

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = chat_with_search(prompt)
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
