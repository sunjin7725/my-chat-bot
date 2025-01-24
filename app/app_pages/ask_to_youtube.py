"""
This file is "Ask to Youtube" app page.
"""

import streamlit as st

from common.streamlit_utils import display_chat_history, talk
from common.ask_for_youtube import get_answer_in_youtube, get_youtube_video_id_from_url

if "video_id" not in st.session_state:
    st.session_state.video_id = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.session_state.video_id = get_youtube_video_id_from_url(st.text_input("Please input youtube video link url."))

display_chat_history(st.session_state.chat_history)

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    with st.chat_message("user"):
        talk(prompt, "user", st.session_state.chat_history)
    with st.chat_message("assistant"):
        response = get_answer_in_youtube(st.session_state.video_id, prompt, st.session_state.chat_history)
        talk(response, "assistant", st.session_state.chat_history)
