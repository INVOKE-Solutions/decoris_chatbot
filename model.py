import pandas as pd
from typing import Union
from langchain_openai import ChatOpenAI
from model_prefix import langchain_prefix
from langchain_core.prompts import MessagesPlaceholder
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    _get_functions_single_prompt,
)
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent


class PandasAgent:
    """
    PandasAgent that can answer user prompt based on dataframe provided.

    Method:
        - `answer_me()` - pass query, chat_history, callback_use (Optional) for agent to answer prompt.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        OPENAI_API_KEY: str,
        prefix: Union[bool, str] = False,
        custom_prefix: Union[str, bool] = False,
        memory=True,
        verbosity: bool = False,
    ):
        """
        Args:
            - df - Pandas dataframe for Agent to infer.
            - OPENAI_API_KEY - OpenAI API key of LLM model
            - prefix -
                - "template" - using prefix template from Langchain
                - "custom" - using customize prefix
                - None - no prefix use, model is unbound
            - custom_prefix - Prefix in string for LLM
            - verbosity - If True, LLM show the Pandas query
        """
        self.openai_api_key = OPENAI_API_KEY
        self.chat_model = ChatOpenAI(
            temperature=0, model="gpt-3.5-turbo", api_key=self.openai_api_key
        )

        self.df = df
        self.verbosity = verbosity
        if prefix == "template":
            self.prefix = langchain_prefix
            # You should use the tools below to answer the question posed of you:
            self.prompt = _get_functions_single_prompt(df, prefix=self.prefix)

        elif prefix == "custom":
            self.prefix = custom_prefix
            self.custom_prefix = custom_prefix
            self.prompt = _get_functions_single_prompt(df, prefix=self.custom_prefix)
        else:
            self.prefix = None
            self.prompt = _get_functions_single_prompt(df)
        self.prompt.input_variables.append("chat_history")
        self.prompt.messages.insert(
            1, MessagesPlaceholder(variable_name="chat_history")
        )

        self.tools = [PythonAstREPLTool(locals={"df": df})]
        self.agent_m = create_openai_functions_agent(
            self.chat_model, self.tools, self.prompt
        )
        self.agent_exe = AgentExecutor(
            agent=self.agent_m, tools=self.tools, verbose=self.verbosity
        )

        self.set_memory = memory
        if self.set_memory:
            self.chat_history = []
        else:
            self.chat_history = None

    def answer_me(
        self, query: str, chat_history: Union[list[object], None], callback_use=None
    ) -> str:
        """
        Return response from the agent by accpet prompt from user.
        Accept callbacks from Streamlit functionality.
        Accept chat_history to save the history of the conversation.

        Args:
            - query : str - user input/question/prompt from user to bot
            - chat_history : list -
                - for Streamlit -  use `st.session_state.chat_history`
                - for API - use `self.chat_history` (`object.chat_history`)
            - callback_use: None - callback from Streamlit. Set `None` if call other than.

        Return:
            - Output - String output from LLM
        """
        if self.set_memory:
            response = self.agent_exe.invoke(
                {"input": query, "chat_history": chat_history}, callbacks=callback_use
            )

            # print(response["output"])
            self.chat_history.extend(
                [
                    HumanMessage(content=query),
                    AIMessage(content=response["output"]),
                ]
            )
        else:
            response = self.agent_exe.invoke({"input": query, "chat_history": []})
        return response["output"]
