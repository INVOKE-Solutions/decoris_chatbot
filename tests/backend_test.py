import streamlit as st
from langchain_openai import ChatOpenAI
from model import PandasAgentWithMemory
from data import Dataset
import pytest
from pathlib import Path
import pandas as pd


# ---------------------------- Dataset ----------------------------------------
@pytest.fixture
def get_dataset():
    dataset = Dataset()
    return dataset


def test_parquet(get_dataset):
    """
    Test the download featurel download parquet from S3
    """
    if not get_dataset.parquet_exist():
        get_dataset.download_parquet()
    assert (
        Path("adsets_v17-11-2023.parquet").exists() == True
    ), "adset parquet not exists"
    assert (
        Path("campaigns_v17-11-2023.parquet").exists() == True
    ), "campaign parquet not exists"


def test_get_merge_df(get_dataset):
    """
    Test to see the merge df is succeed
    """
    if get_dataset.parquet_exist():
        assert isinstance(
            get_dataset.get_merge_df(), pd.DataFrame
        ), "Output is not dataframe"
    else:
        raise "parquet is not exist"
    df_col = get_dataset.get_merge_df().columns
    assert "Campaign ID" in df_col, "Campaign ID column not exist in merged dataframe"
    assert "Adset Name" in df_col, "Adset name column is not exist in merged dataframe"


# --------------------------- Model ------------------------------------------
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
chat_model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)


def test_invoke_model(get_dataset):
    agent = PandasAgentWithMemory(get_dataset.get_merge_df())
    user_input = "Who are you?"
    response = agent.answer_me(user_input, agent.chat_history, None)
    assert isinstance(response, str), "Response is not string"
