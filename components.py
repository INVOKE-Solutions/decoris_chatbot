import time
import streamlit as st
from backend import load_parquet

def side_bar():
    with st.sidebar:
        st.subheader("Refresh data")
        refresh_button = st.button("Refresh")
        progress_bar = st.progress(0)
        if refresh_button:
            load_parquet()
            for i in range(100):
                time.sleep(0.001)
                progress_bar.progress(i+1)
            time.sleep(0.5)
            st.success("Refresh complete")

def page_title(title:str):
    st.title(title)