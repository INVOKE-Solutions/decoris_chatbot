import streamlit as st
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from langchain.agents import AgentExecutor, create_openai_functions_agent  # x
from langchain_core.messages import AIMessage, HumanMessage  # x
from langchain_core.prompts import MessagesPlaceholder  # x
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    _get_functions_single_prompt,
)  # x
from langchain_experimental.tools.python.tool import PythonAstREPLTool  # x
from langchain_openai import ChatOpenAI


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


class PandasAgentWithMemory:
    def __init__(self, df):
        self.df = df
        self.prompt = _get_functions_single_prompt(df)  # idk, param: dataframe
        self.prompt.input_variables.append("chat_history")
        self.prompt.messages.insert(
            1, MessagesPlaceholder(variable_name="chat_history")
        )
        # MessagePlaceholder - prompt template that assume variable is already list of message

        self.tools = [
            PythonAstREPLTool(locals={"df": df})
        ]  # REPL - to ensure it can run the code in REPL (the pandas line)
        # tools - interact with dataframe

        self.agent_m = create_openai_functions_agent(
            chat_model, self.tools, self.prompt
        )  # create agent
        self.agent_exe = AgentExecutor(
            agent=self.agent_m, tools=self.tools, verbose=True
        )  # connect agent and tools

        self.chat_history = []

    def answer_me(self, query, chat_history: list, cb):
        response = self.agent_exe.invoke(
            {"input": query, "chat_history": chat_history}, callbacks=cb
        )
        # self.chat_history.extend(
        #     [
        #         HumanMessage(content=query),  # BaseMessage for Human
        #         AIMessage(content=response["output"]),  # BaseMessage for AI
        #     ]
        # )

        return response["output"]
