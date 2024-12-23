# app/utils/streamlit_helpers.py

import streamlit as st
from contextlib import contextmanager

@contextmanager
def create_spinner(text):
    with st.spinner(text):
        yield