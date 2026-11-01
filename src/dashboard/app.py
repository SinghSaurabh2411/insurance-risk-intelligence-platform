"""Insurance Risk Intelligence Platform Streamlit dashboard."""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

st.set_page_config(
    page_title="Insurance Risk Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Insurance Risk Intelligence Platform")
st.caption("Portfolio analytics and insurance risk intelligence")
st.divider()
st.info(
    "Dashboard foundation is ready. API integration and analytical views "
    "will be added in the next steps."
)
st.sidebar.title("Navigation")
st.sidebar.caption("Dashboard sections will appear here as they are developed.")
