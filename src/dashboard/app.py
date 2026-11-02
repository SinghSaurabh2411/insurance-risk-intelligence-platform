"""Insurance Risk Intelligence Platform Streamlit dashboard."""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import streamlit as st

from dashboard.api_client import DashboardAPIClient, DashboardAPIError

st.set_page_config(
    page_title="Insurance Risk Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=300, show_spinner=False)
def load_overview_data() -> tuple[dict, dict]:
    """Fetch portfolio summary and yearly metrics through the existing API."""
    client = DashboardAPIClient()
    return client.get_summary(), client.get_yearly()


def format_currency_millions(value: float) -> str:
    """Format a currency amount as Indian rupees in millions."""
    return f"₹{value / 1_000_000:,.2f}M"


def render_kpis(summary: dict) -> None:
    """Render the six portfolio-level KPI cards."""
    metrics = [
        ("Total policies", f"{summary['total_policies']:,}"),
        ("Total observations", f"{summary['total_observations']:,}"),
        ("Total premium", format_currency_millions(summary["total_premium"])),
        ("Total claims cost", format_currency_millions(summary["total_claims_cost"])),
        ("Average premium", f"₹{summary['average_premium']:,.2f}"),
        ("Total exposure", f"{summary['total_exposure']:,.2f}"),
    ]

    columns = st.columns(6)
    for column, (label, value) in zip(columns, metrics):
        column.metric(label=label, value=value)


def render_yearly_trends(yearly: dict) -> None:
    """Render yearly premium, claims-cost, and exposure trends."""
    years = yearly.get("years", [])
    if not years:
        st.info("No yearly performance data is currently available.")
        return

    frame = pd.DataFrame(years).sort_values("period")
    frame["premium_m"] = frame["total_premium"] / 1_000_000
    frame["claims_cost_m"] = frame["total_claims_cost"] / 1_000_000

    premium_col, claims_col, exposure_col = st.columns(3)
    with premium_col:
        st.subheader("Premium")
        st.line_chart(
            frame,
            x="period",
            y="premium_m",
            y_label="₹ millions",
        )
    with claims_col:
        st.subheader("Claims cost")
        st.line_chart(
            frame,
            x="period",
            y="claims_cost_m",
            y_label="₹ millions",
        )
    with exposure_col:
        st.subheader("Exposure")
        st.line_chart(
            frame,
            x="period",
            y="total_exposure",
            y_label="Exposure",
        )


st.title("Insurance Risk Intelligence Platform")
st.caption("Portfolio analytics and insurance risk intelligence")

with st.sidebar:
    st.title("Navigation")
    st.caption("Portfolio overview")
    if st.button("Refresh dashboard", use_container_width=True):
        load_overview_data.clear()
        st.rerun()

try:
    with st.spinner("Loading portfolio analytics..."):
        summary_data, yearly_data = load_overview_data()

    st.subheader("Portfolio overview")
    render_kpis(summary_data)

    st.divider()
    st.subheader("Yearly performance trends")
    render_yearly_trends(yearly_data)

    st.caption("Data source: Gold layer via the authenticated Insurance Risk Intelligence API.")
except DashboardAPIError as exc:
    st.error(f"Unable to load dashboard data: {exc}")
    st.info(
        "Confirm that FastAPI is running and that API_ACCESS_KEY is configured "
        "for this Streamlit process."
    )
except RuntimeError as exc:
    st.error(f"Dashboard configuration error: {exc}")
