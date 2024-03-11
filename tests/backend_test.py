import streamlit as st
from langchain_openai import ChatOpenAI
from model import PandasAgentWithMemory
from data import Dataset
import pytest
from pathlib import Path
import pandas as pd
from rename_map import fb_page_category_mapping, client_industry_mapping


# ---------------------------- Dataset ----------------------------------------
@pytest.fixture
def get_dataset() -> Dataset:
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


@pytest.fixture
def get_merge_df(get_dataset):
    merge_df = get_dataset.get_merge_df()
    return merge_df


def test_handling_empty_nan(get_dataset, get_merge_df: pd.DataFrame):
    df_no_null = get_dataset.handle_empty_nan(get_merge_df)

    def check_no_null(col_name: str) -> bool:
        if (
            "" not in df_no_null[col_name].unique()
            and " " not in df_no_null[col_name].unique()
        ):
            return True

    assert "All" in df_no_null["Gender"].unique(), "No All in Gender column"
    assert (
        check_no_null("Custom Audiences") == True
    ), "There is blank value in Custom Audience column"

    assert (
        check_no_null("Company Name") == True
    ), "There is blank value in Company Name column"
    assert (
        check_no_null("Client Industry") == True
    ), "There is blank value in Client Industry column"
    assert (
        check_no_null("Psychographic") == True
    ), "There is blank value in Psychographic column"
    assert (
        check_no_null("Facebook Page Name") == True
    ), "There is blank value in book Page Name column"
    assert check_no_null("Country") == True, "There is blank value in Country column"


def test_client_industry_rename(get_dataset, get_merge_df):
    renamed_df = get_dataset.rename_client_industry(get_merge_df)
    assert (
        list(client_industry_mapping.values())[0]
        in renamed_df["Client Industry"].unique()
    ), f"{list(client_industry_mapping.values())[0]} not exist in Client Industry unique value"


def test_facebook_page_category_rename(get_dataset, get_merge_df):
    rename_df = get_dataset.rename_fb_page_category(get_merge_df)
    assert (
        list(fb_page_category_mapping.values())[0]
        in rename_df["Facebook Page Category"].unique()
    ), f"{list(fb_page_category_mapping.values())[0]} not in Facebook Page Category uniquer value"


# --------------------------- Model ------------------------------------------
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
chat_model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)


def test_invoke_model(get_dataset):
    agent = PandasAgentWithMemory(get_dataset.get_merge_df())
    user_input = "Who are you?"
    response = agent.answer_me(user_input, agent.chat_history, None)
    assert isinstance(response, str), "Response is not string"
