from pathlib import Path

import streamlit as st


def load_css(file_path: Path):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
