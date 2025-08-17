from pathlib import Path

import streamlit as st

from src.assests.load import load_css

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")


load_css(Path("src/assests/styles.css"))


def on_login_click():
    st.login()


def on_logout_click():
    st.logout()


with st.container():

    if not st.user.is_logged_in:
        st.title("Login to CVRAGent")
        st.subheader("Sign in with your Google account")
        st.button(
            "Log in with Google",
            type="primary",
            icon=":material/login:",
            use_container_width=True,
            on_click=on_login_click,
        )
    else:
        st.markdown(
            f'<div class="title">Hello, <span style="color: #45a049;">{st.user.name}</span>!</div>',
            unsafe_allow_html=True,
        )
        st.subheader("You are now logged in.")
        st.button(
            "Log out", type="primary", icon=":material/logout:", use_container_width=True, on_click=on_logout_click
        )
