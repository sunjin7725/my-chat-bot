"""
This file is "Ask to Youtube" app page.
"""

import streamlit as st

from utils.ask_for_youtube import get_answer_in_youtube, get_youtube_video_id_from_url


TITLE = "Ask to Youtube"
st.set_page_config(layout="wide", page_title=TITLE, page_icon="🦒")

st.markdown(f"# {TITLE}")

if "video_id" not in st.session_state:
    st.session_state.video_id = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.session_state.video_id = get_youtube_video_id_from_url(st.text_input("Please input youtube video link url."))

for content in st.session_state.chat_history:
    with st.chat_message(content["role"]):
        st.markdown(content["message"])

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "message": prompt})
    with st.chat_message("assistant", avatar="🤖"):
        response = get_answer_in_youtube(st.session_state.video_id, prompt)
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "message": response})
