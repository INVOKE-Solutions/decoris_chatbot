import time
import streamlit as st
from data import Dataset
from css_template import user_template, bot_template


def side_bar():
    data = Dataset()
    with st.sidebar:
        st.subheader("Refresh data")
        refresh_button = st.button("Refresh")
        progress_bar = st.progress(0)
        if refresh_button:
            data.load_parquet()
            for i in range(100):
                time.sleep(0.001)
                progress_bar.progress(i + 1)
            time.sleep(0.5)
            st.success("Refresh complete")


def page_title(title: str):
    st.title(title)


def initial_chat_history_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def show_chat_dialogue(chat_history: list):
    """
    Initialize state to ensure the apps
    remember the conversation.

    """
    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", f"{message}"),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", f"🤖-- {message}"),
                unsafe_allow_html=True,
            )
