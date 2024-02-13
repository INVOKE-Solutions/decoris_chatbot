import streamlit as st
from components import side_bar, page_title

st.set_page_config(page_title="Decoris Chatbot", page_icon="🤖")


page_title("Decoris Chatbot with LLM")
side_bar()

user_input = st.chat_input("Ask about the Campaign, Adset or Ads!")
