from pathlib import Path
import streamlit as st
import boto3

def load_parquet():
    bucket_name = st.secrets["BUCKET_NAME"]
    object_name_1 = st.secrets["OBJECT_NAME_1"]
    object_name_2 = st.secrets["OBJECT_NAME_2"]


    root_path = Path.cwd()

    parq_path = root_path / object_name_1
    s3_object_list = [object_name_1, object_name_2]
    s3 = boto3.client('s3')

    if not parq_path.exists():
        for obj in s3_object_list:
            s3.download_file(bucket_name,
                            obj,
                            obj,
                            )
            print(f"STATUS: {obj} is downloaded")
            
    print("download completed")