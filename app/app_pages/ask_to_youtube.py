"""
This file is "Ask to Youtube" app page.
"""

import streamlit as st

from common.ask_for_youtube import get_answer_in_youtube, get_youtube_video_id_from_url

if "video_id" not in st.session_state:
    st.session_state.video_id = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.session_state.video_id = get_youtube_video_id_from_url(st.text_input("Please input youtube video link url."))

for content in st.session_state.chat_history:
    with st.chat_message(content["role"]):
        st.markdown(content["content"])

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = get_answer_in_youtube(st.session_state.video_id, prompt, st.session_state.chat_history)
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
