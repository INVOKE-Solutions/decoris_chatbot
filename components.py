import time
import streamlit as st
from data import Dataset
from css_template import user_template, bot_template
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.callbacks import StreamlitCallbackHandler
from model import PandasAgentWithMemory


def side_bar():
    """
    UI: Sidebar
    - Refresh button: Download dataset into server
    """
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
    """UI: Page title"""
    st.title(title)


def initial_chat_history_state():
    """
    Session sate: Chat history
    - If not instantiate, create a list as chat history
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def update_chat_history(user_input: str, bot_response: str):
    """
    Session state: Chat history
    - Update chat history with user_input and bot_response

    Args:
    - user_input: str - User input from Streamlit
    - bot_response: str - Bot response from agent response
    """
    st.session_state.chat_history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=bot_response),
        ]
    )


def handle_bot_response(
    agent: PandasAgentWithMemory, user_input: str, chat_history: list
) -> str:
    """
    Args:
    - agent: PandasAgentWithMemory - Agent to asnwer question
    - user_input: User input from Streamlit input
    - chat_history: list - st.session_state.chat_history - chat history

    Return:
    - response: str - response from agent
    """
    st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    response = agent.answer_me(user_input, chat_history=chat_history, cb=[st_callback])
    return response


def show_chat_dialogue(chat_history: list):
    """
    UI: Chat message dialogue

    Arg:
    - chat_history: list - st.session_state.chat_history

    Return:
    - Streamlit chat message from user and bot

    """
    for i, chat in enumerate(chat_history):
        if i % 2 == 0:
            st.chat_message("user").write(chat.content)
        else:
            with st.chat_message("🤖"):
                st.write(chat.content)
