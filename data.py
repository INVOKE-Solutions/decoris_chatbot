from pathlib import Path
import streamlit as st
import boto3
import pandas as pd

AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]


class Dataset:
    """
    Class Dataset to download dataset from AWS S3, process and return the final dataframe.
    """

    def __init__(self):
        self.root_path = Path.cwd()
        self.bucket_name = st.secrets["BUCKET_NAME"]
        self.campaign_parquet = st.secrets["OBJECT_NAME_1"]
        self.adset_parquet = st.secrets["OBJECT_NAME_2"]

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
