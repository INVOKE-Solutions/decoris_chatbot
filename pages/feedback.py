import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from components import initialize_login_state
from datetime import datetime
from pages.login import read_pickle, get_login_pickle

# datetime object containing current date and time
now = datetime.now()
date_data = now.strftime("%d/%m/%Y")
time_data = now.strftime("%H:%M:%S")


def connect_gsheet() -> GSheetsConnection:
    """
    Create connection to google sheets
    Please ensure to keep all key from GCP within secrets.toml (local)
    or Secrets Management (Streamlit secret management)
    """
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn


def read_gsheet(conn: GSheetsConnection) -> pd.DataFrame:
    """
    Read current Googel Spreadsheet table.

    Args:
    - conn - connection from `connect_gshee()`
    """
    df = conn.read(
        worksheet="feedback", usecols=["Date", "Time", "Name", "User Feedback"]
    )
    return df


def insert_gsheet(
    conn: GSheetsConnection, user_name: str, user_feedback: str, old_df: pd.DataFrame
) -> None:
    """
    Insert new data into Google Sheet table.

    Args:
    - conn : GSheetsConnection - Google Sheet connection
    - user_name: str - User's name that provide feedback
    - user_feedback: str - User's feedback
    - old_df: pd.DataFrame: old table to be concat with new data

    """
    new_df = pd.DataFrame(
        {
            "Date": [date_data],
            "Time": [time_data],
            "Name": [user_name],
            "User Feedback": [user_feedback],
        }
    )
    current_df = pd.concat([old_df.dropna(), new_df])
    conn.update(worksheet="feedback", data=current_df)


def user_feedback():
    pickle_dict = read_pickle()

    initialize_login_state()

    if st.session_state.login or get_login_pickle(pickle_dict):
        st.title("Feedback")
        st.write("Tell us your feedback on the apps!")
        # Establish connection
        conn = connect_gsheet()

        with st.form("Submit form"):

            # Input user name and user feedback
            user_name = st.text_input("Name")
            user_feedback = st.text_area(
                label="Feedback",
                value="It can be additional feature, comment, or anything...",
            )

            submit_button = st.form_submit_button("Submit")

            # get currect table
            old_df = read_gsheet(conn)
            if submit_button:
                insert_gsheet(conn, user_name, user_feedback, old_df=old_df)
                st.balloons()
                st.success("Thank you for your feedback!")

        with st.expander("See feedback"):
            # clear data in Streamlit to see the current table
            st.cache_data.clear()
            st.write(read_gsheet(conn).dropna())

    elif not st.session_state.login and not get_login_pickle(pickle_dict):
        st.warning("Please login first")


if __name__ == "__main__":
    user_feedback()
