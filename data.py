import os
import boto3
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from rename_map import client_industry_mapping, fb_page_category_mapping

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class Dataset:
    """
    Class Dataset to download dataset from AWS S3, process and return the final dataframe.
    """

    def __init__(self):
        self.root_path = Path.cwd()
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.campaign_parquet = os.getenv("OBJECT_NAME_1")
        self.adset_parquet = os.getenv("OBJECT_NAME_2")

    def download_parquet(self):
        """
        Download parquet from AWS S3. Ask AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        from devops/backend engineer to get the access permission.
        """

        s3_object_list = [self.campaign_parquet, self.adset_parquet]
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # if not parq_path.exists():
        for obj in s3_object_list:
            s3.download_file(
                self.bucket_name,
                obj,
                obj,
            )
            print(f"STATUS: {obj} is downloaded")

        print("STATUS: Download completed")

    def read_parquet(self, parque_name: str) -> pd.DataFrame:
        """
        Read parquet file downloaded as Pandas Dataframe.
        """
        return pd.read_parquet(parque_name)

    def merge_df(self, df_1: pd.DataFrame, df_2: pd.DataFrame):
        """
        Merge 2 dataframe from the parquet into a single by left join.

        Args:
        - df_1: pd.DataFrame - left
        - df_2: pd.DataFrame - right

        Return:
        - camp_adset_df: pd.DataFrame - joined dataframe

        """
        camp_adset_df = df_1.merge(
            df_2, on="Campaign ID", how="left", suffixes=("", "_DROP")
        ).filter(regex="^(?!.*_DROP)")
        return camp_adset_df

    @st.cache_data(ttl="1d")
    def get_merge_df(_self) -> pd.DataFrame:
        """
        Return merge dataset from 2 dataframe
        """
        adset_df = _self.read_parquet(_self.root_path / _self.adset_parquet)
        campaign_df = _self.read_parquet(_self.root_path / _self.campaign_parquet)
        merge_df = _self.merge_df(adset_df, campaign_df)
        return merge_df

    def parquet_exist(self) -> bool:
        """
        Return True if adset_parquet exist.
        """
        parq_path = self.root_path / self.adset_parquet
        if parq_path.exists():
            return True


class DataFrameCleaning:
    """
    Clean dataframe by
        - Handling nan and empty value
        - Rename Client Industry column
        - Rename Facebook Page Category column

    """

    def __init__(self, merge_df):
        """
        Args:
            - merge_df  - Merged dataframe from `Dataset.get_merge_df()`
        """
        self.merge_df = merge_df

    def handle_empty_nan(self, merge_df) -> pd.DataFrame:
        """
        Handling empty, NAN

        Details:
        - "Gender" - replace blank with "All"
        -  Others:
                - Replace `null` with `np.NAN`
                - Replace blank with `np.NAN`
        """

        def fillna_replace(df, column_name: str, replace_val):
            df_replace = (
                df[[column_name]]
                .fillna(replace_val)
                .replace(r"^\s*$", replace_val, regex=True)
            )
            return df_replace

        merge_df["Gender"] = fillna_replace(merge_df, "Gender", "All")
        merge_df["Custom Audiences"] = fillna_replace(
            merge_df, "Custom Audiences", np.NAN
        )
        merge_df["Country"] = fillna_replace(merge_df, "Country", np.NAN)
        merge_df["Company Name"] = merge_df["Company Name"].fillna(np.NAN)
        merge_df["Client Industry"] = fillna_replace(
            merge_df, "Client Industry", np.NAN
        )
        merge_df["Psychographic"] = fillna_replace(merge_df, "Psychographic", np.NAN)
        merge_df["Facebook Page Name"] = fillna_replace(
            merge_df, "Facebook Page Name", np.NAN
        )
        return merge_df

    def rename_client_industry(self, merge_df: pd.DataFrame) -> pd.DataFrame:
        """
        Return dataframe with rename value
        """
        merge_df = merge_df.replace(client_industry_mapping)
        return merge_df

    def rename_fb_page_category(self, merge_df: pd.DataFrame) -> pd.DataFrame:
        """
        Return dataframe with rename value
        """
        merge_df = merge_df.replace(fb_page_category_mapping)
        return merge_df

    def clean_df(self) -> pd.DataFrame:
        """
        Return the final clean dataframe
        """
        handle_df = self.handle_empty_nan(self.merge_df)
        rename_client_df = self.rename_client_industry(handle_df)
        rename_fb_df = self.rename_fb_page_category(rename_client_df)

        return rename_fb_df
