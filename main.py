import streamlit as st
from components import (
    side_bar,
    page_title,
    initial_chat_history_state,
    show_chat_dialogue,
)
from model import create_agent, ask_agent
from data import Dataset
from css_template import css
from langchain.memory import ConversationBufferMemory


def main():
    st.set_page_config(page_title="Decoris Chatbot", page_icon="🤖")

    page_title("Decoris Chatbot with LLM")
    side_bar()

    data = Dataset()
    if not data.parquet_exist():
        data.download_parquet()

    # initial state
    initial_chat_history_state()

    agent = create_agent(dataset=data.get_merge_df())
    st.write(css, unsafe_allow_html=True)
    user_input = st.chat_input("Ask about the Campaign, Adset or Ads!")

    if user_input:
        st.session_state.chat_history.append(user_input)
        agent_response = ask_agent(agent, st.session_state.chat_history)
        st.session_state.chat_history.append(agent_response["output"])

        show_chat_dialogue(st.session_state.chat_history)


if __name__ == "__main__":
    main()
