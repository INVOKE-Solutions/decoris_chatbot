import streamlit as st
import pickle
from pathlib import Path

root_path = Path.cwd()
LOGIN_PICKLE_PATH = root_path / "login.pkl"


def pickle_login(username, password):
    login_data = {"username": username, "password": password}
    pickle_out = open("login.pkl", "wb")
    pickle.dump(login_data, pickle_out)
    pickle_out.close()


def login():
    with st.form("Login", border=False):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if (
                username == st.secrets["USERNAME"]
                and password == st.secrets["PASSWORD"]
            ):
                st.success(f"Welcome {username}")
                st.session_state.login = True
                st.session_state.username = username
                st.session_state.password = password
                pickle_login(username, password)
                return True
            else:
                st.error("Username/password is incorrect")
        else:
            st.warning("Please enter username and password")


if __name__ == "__main__":
    login()
