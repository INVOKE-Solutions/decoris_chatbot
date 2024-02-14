import streamlit as st
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
chat_model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)


def create_agent(dataset: pd.DataFrame, verbosity=False):
    agent = create_pandas_dataframe_agent(
        chat_model,
        dataset,
        verbose=verbosity,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        agent_executor_kwargs={"handle_parsing_errors": True},
    )
    return agent


def ask_agent(agent, prompt):
    output = agent.invoke(prompt)
    return output
