import streamlit as st
from components import side_bar, page_title
from model import create_agent, ask_agent
from data import Dataset

def main():
    st.set_page_config(page_title="Decoris Chatbot", page_icon="🤖")


    page_title("Decoris Chatbot with LLM")
    side_bar()

    data = Dataset()
    if not data.parquet_exist():
        data.load_parquet()
    
    agent = create_agent(dataset=data.get_merge_df())

    user_input = st.chat_input("Ask about the Campaign, Adset or Ads!")
    if user_input:
        response = ask_agent(agent, user_input)
        st.write(response)

if __name__ == "__main__":
    main()
