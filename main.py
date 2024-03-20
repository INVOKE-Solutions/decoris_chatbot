import streamlit as st
from components import (
    side_bar,
    page_title,
    show_chat_dialogue,
    update_chat_history,
    handle_bot_response,
    initialize_login_state,
    initialize_chat_history_state,
)
from data import Dataset
from model import PandasAgent
from st_pages import show_pages, Page

# Rearrange page order
show_pages(
    [
        Page("pages/login.py", "Login", "🔐"),
        Page("pages/feedback.py", "Feedback", "📩"),
        Page("main.py", "Chatbot", "🤖"),
    ]
)

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def main():
    initialize_login_state()
    if st.session_state.login:
        page_title("Decoris Chatbot 🤖")
        side_bar()

        # download data
        data = Dataset()
        if not data.parquet_exist():
            data.download_parquet()

        # initial state
        initialize_chat_history_state()

        # create agent (model)
        agent = PandasAgent(
            df=data.get_merge_df(),
            prefix=False,
            memory=True,
            OPENAI_API_KEY=OPENAI_API_KEY,
        )

        # user input feature
        user_input = st.chat_input("Ask about the Campaign, Adset or Ads!")

        if user_input:
            bot_response = handle_bot_response(
                agent, user_input, chat_history=st.session_state.chat_history
            )
            update_chat_history(user_input, bot_response)
            show_chat_dialogue(st.session_state.chat_history)

    elif not st.session_state.login:
        st.warning("Please login first")


if __name__ == "__main__":
    st.set_page_config(page_title="Decoris Chatbot", page_icon="🤖")

    main()
