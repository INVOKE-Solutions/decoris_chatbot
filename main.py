import streamlit as st
from components import (
    side_bar,
    page_title,
    initial_chat_history_state,
    show_chat_dialogue,
    update_chat_history,
)
from model import create_agent, ask_agent, PandasAgentWithMemory
from data import Dataset
from css_template import css
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


def main():
    st.set_page_config(page_title="Decoris Chatbot", page_icon="🤖")

    page_title("Decoris Chatbot with LLM 🤖")
    side_bar()

    data = Dataset()
    if not data.parquet_exist():
        data.download_parquet()

    # initial state
    initial_chat_history_state()

    agent = PandasAgentWithMemory(data.get_merge_df())
    st.write(css, unsafe_allow_html=True)
    user_input = st.chat_input("Ask about the Campaign, Adset or Ads!")

    if user_input:
        st.chat_message("user").write(user_input)

        with st.chat_message("🤖"):
            st_callback = StreamlitCallbackHandler(
                st.container(), expand_new_thoughts=False
            )
            response = agent.answer_me(
                user_input, chat_history=st.session_state.chat_history, cb=[st_callback]
            )
            update_chat_history(user_input, response)
            st.write(response)


if __name__ == "__main__":
    main()
