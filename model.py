import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    _get_functions_single_prompt,
)
from langchain.agents import AgentExecutor, create_openai_functions_agent


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
chat_model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)


class PandasAgentWithMemory:
    def __init__(self, df):
        self.df = df
        self.prompt = _get_functions_single_prompt(df)
        self.prompt.input_variables.append("chat_history")
        self.prompt.messages.insert(
            1, MessagesPlaceholder(variable_name="chat_history")
        )

        self.tools = [PythonAstREPLTool(locals={"df": df})]

        self.agent_m = create_openai_functions_agent(
            chat_model, self.tools, self.prompt
        )
        self.agent_exe = AgentExecutor(
            agent=self.agent_m, tools=self.tools, verbose=True
        )

        self.chat_history = []

    def answer_me(self, query, chat_history: list, callback_use=None):
        """
        Return response from the agent by accpet prompt from user.
        Accept callbacks from Streamlit functionality.
        Accept chat_history to save the history of the conversation.

        Args:
        - query : str - user input/question/prompt from user to bot
        - chat_history : list -
            - for Streamlit -  use `st.session_state.chat_history`
            - for API - use `self.chat_history` (`object.chat_history`)
        - callback_use: None - callback from Streamlit. `None` if call outside Streamlit.
        """
        response = self.agent_exe.invoke(
            {"input": query, "chat_history": chat_history}, callbacks=callback_use
        )
        return response["output"]
