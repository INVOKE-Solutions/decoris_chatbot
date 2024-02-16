import streamlit as st
from components import (
    side_bar,
    page_title,
    initial_chat_history_state,
    show_chat_dialogue,
    update_chat_history,
    handle_bot_response,
)
import time
from model import create_agent, ask_agent, PandasAgentWithMemory
from data import Dataset
from css_template import css
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


def main():
    st.set_page_config(page_title="Decoris Chatbot", page_icon="🤖")

    page_title("Decoris Chatbot with LLM 🤖")
    side_bar()

    # download data
    data = Dataset()
    if not data.parquet_exist():
        data.download_parquet()

    # initial state
    initial_chat_history_state()

    # create agent (model)
    agent = PandasAgentWithMemory(data.get_merge_df())
    st.write(css, unsafe_allow_html=True)

    # user input feature
    user_input = st.chat_input("Ask about the Campaign, Adset or Ads!")

    if user_input:
        bot_response = handle_bot_response(
            agent, user_input, chat_history=st.session_state.chat_history
        )
        update_chat_history(user_input, bot_response)
        show_chat_dialogue(st.session_state.chat_history)


if __name__ == "__main__":
    main()
