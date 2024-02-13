from pathlib import Path
import streamlit as st
import boto3
import pandas as pd

AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]

def load_parquet():
    bucket_name = st.secrets["BUCKET_NAME"]
    object_name_1 = st.secrets["OBJECT_NAME_1"]
    object_name_2 = st.secrets["OBJECT_NAME_2"]


    root_path = Path.cwd()

    parq_path = root_path / object_name_1
    s3_object_list = [object_name_1, object_name_2]
    s3 = boto3.client('s3',
                    aws_access_key_id = AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

    if not parq_path.exists():
        for obj in s3_object_list:
            s3.download_file(bucket_name,
                            obj,
                            obj,
                            )
            print(f"STATUS: {obj} is downloaded")

    print("download completed")

def read_parquet(parque_name:str):
    return pd.read_parquet(parque_name)

def merge_df(df_1, df_2):
    camp_adset_df = df_1.merge(df_2, on="Campaign ID", 
                                how="left", 
                                suffixes=('', '_DROP'))\
                .filter(regex='^(?!.*_DROP)')
    return camp_adset_df

def get_merge_df():
    adset_df = read_parquet("adsets_v17-11-2023.parquet")
    campaign_df = read_parquet("campaigns_v17-11-2023.parquet")

    merge_df = merge_df(adset_df, campaign_df)
    return merge_df
