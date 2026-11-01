"""Server-side configuration for the Streamlit dashboard."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_api_base_url() -> str:
    """Return the FastAPI base URL."""
    value = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").strip()
    return value.rstrip("/")


def get_api_access_key() -> str:
    """Return the API key from environment variables or Streamlit secrets."""
    value = os.getenv("API_ACCESS_KEY", "").strip()
    if not value:
        try:
            import streamlit as st
            value = str(st.secrets.get("API_ACCESS_KEY", "")).strip()
        except Exception:
            value = ""
    if not value:
        raise RuntimeError(
            "API_ACCESS_KEY is not configured. Set it in the local .env file "
            "or Streamlit secrets."
        )
    return value
