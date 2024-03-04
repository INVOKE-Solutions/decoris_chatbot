import streamlit as st


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
                return True
            else:
                st.error("Username/password is incorrect")
        else:
            st.warning("Please enter username and password")


if __name__ == "__main__":
    login()
