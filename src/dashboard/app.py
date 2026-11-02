"""Insurance Risk Intelligence Platform Streamlit dashboard."""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import altair as alt
import pandas as pd
import streamlit as st

from dashboard.api_client import DashboardAPIClient, DashboardAPIError

st.set_page_config(
    page_title="Insurance Risk Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Saturated, high-contrast palette shared consistently across dashboard pages.
COLORS = {
    "blue": "#2563EB",
    "orange": "#F97316",
    "teal": "#0F9D8A",
    "purple": "#7C3AED",
    "pink": "#DB2777",
}
CHART_PALETTE = [
    "#2563EB", "#F97316", "#0F9D8A", "#7C3AED",
    "#DB2777", "#0891B2", "#CA8A04", "#4F46E5",
]
METRIC_HELP = {
    "Total policies": (
        "Number of distinct insurance policy IDs represented in the data. "
        "A policy appearing in multiple periods is counted once in an overall total."
    ),
    "Total observations": (
        "Number of policy-insured-period records in the Gold FACT_POLICY table. "
        "A policy can contribute multiple observations across periods or insured members."
    ),
    "Total premium": "Sum of premium amounts across the selected records.",
    "Total claims cost": "Sum of the recorded yearly claims-cost amounts across the selected records.",
    "Average premium": "Arithmetic average of premium per policy-insured-period observation; it is not the average per unique policy.",
    "Total exposure": "Sum of exposure time across the selected records. Interpret this using the source dataset's exposure-time unit.",
    "Customer records": "Distinct customer dimension records represented in the selected observations.",
    "Period covered": "The earliest and latest reporting years available in the returned yearly dataset.",
}
PAGE_DESCRIPTIONS = {
    "Portfolio overview": "A high-level view of the insurance portfolio and its yearly movement.",
    "Product analysis": "Compares portfolio performance across product type and reimbursement category.",
    "Channel analysis": "Shows how premium, claims cost, and portfolio volume are distributed across sales channels.",
    "Policy analysis": "Compares portfolio performance across policy type and policy DG classification.",
    "Customer analysis": "Breaks down the portfolio by the gender attribute available in the customer dimension.",
    "Customer cohort analysis": "Compares insured customer records by the year their insurance became effective.",
}

st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff 0%, #f5f8ff 100%);
        border: 1px solid #e5eaf4;
        border-left: 5px solid #3977d5;
        padding: 14px 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(25, 45, 80, 0.06);
    }
    [data-testid="stMetricLabel"] { color: #52627a; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #172b4d; }
    h1 { color: #17365f; }
    .definition-icon {
        display: inline-block;
        margin-left: 4px;
        color: #3977d5;
        border: 1px solid #9bb8e8;
        border-radius: 50%;
        width: 16px;
        height: 16px;
        line-height: 15px;
        text-align: center;
        font-size: 11px;
        font-weight: 700;
        cursor: help;
        vertical-align: middle;
    }
    .page-intro { color: #64748b; margin-top: -8px; margin-bottom: 18px; }
    [data-testid="stVegaLiteChart"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8faff 100%);
        border: 1px solid #e1e8f5;
        border-radius: 12px;
        padding: 8px 8px 2px 8px;
        box-shadow: 0 3px 12px rgba(31, 55, 95, 0.07);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def load_endpoint(endpoint_name: str) -> dict:
    """Fetch one analytics resource through the authenticated API client."""
    client = DashboardAPIClient()
    methods = {
        "summary": client.get_summary,
        "yearly": client.get_yearly,
        "products": client.get_products,
        "channels": client.get_channels,
        "policies": client.get_policies,
        "customers": client.get_customers,
        "customer_cohorts": client.get_customer_cohorts,
    }
    return methods[endpoint_name]()


def format_currency_millions(value: float) -> str:
    return f"₹{value / 1_000_000:,.2f}M"


def info_heading(label: str, definition: str) -> None:
    """Show a compact heading with a hover-only definition icon."""
    st.markdown(
        f'<div style="font-size:1rem;font-weight:650;margin:0 0 8px 0;">'
        f'{label}<span class="definition-icon" title="{definition}">i</span></div>',
        unsafe_allow_html=True,
    )


def render_metric_row(metrics: list[tuple[str, str, str]]) -> None:
    """Render KPI cards with Streamlit's built-in hover help icons."""
    columns = st.columns(len(metrics))
    for column, (label, value, help_text) in zip(columns, metrics):
        column.metric(label=label, value=value, help=help_text)


def render_bar_chart(
    data: pd.DataFrame,
    category: str,
    value: str,
    title: str,
    color: str,
    value_title: str,
    *,
    horizontal: bool = False,
    height: int = 330,
) -> None:
    """Render a labelled bar chart with readable axes and exact-value tooltips."""
    chart_data = data.copy()
    chart_data[category] = chart_data[category].fillna("Not available").astype(str)
    chart_data[value] = pd.to_numeric(chart_data[value], errors="coerce").fillna(0)
    if chart_data.empty:
        st.info("No data is available for this chart.")
        return

    if horizontal:
        bars = alt.Chart(chart_data).mark_bar(
            color=color, opacity=0.96, cornerRadiusEnd=5,
            stroke=color, strokeWidth=0.4,
        ).encode(
            y=alt.Y(
                f"{category}:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelFontWeight="bold", labelLimit=220),
            ),
            x=alt.X(
                f"{value}:Q",
                title=value_title,
                axis=alt.Axis(labelFontWeight="bold", titleFontWeight="bold"),
            ),
            tooltip=[
                alt.Tooltip(f"{category}:N", title=title),
                alt.Tooltip(f"{value}:Q", title=value_title, format=",.2f"),
            ],
        )
        labels = alt.Chart(chart_data).mark_text(
            align="left", baseline="middle", dx=5, fontWeight="bold", color="#34445B"
        ).encode(
            y=alt.Y(f"{category}:N", sort="-x"),
            x=alt.X(f"{value}:Q"),
            text=alt.Text(f"{value}:Q", format=",.2f"),
        )
        chart = (bars + labels).properties(height=height)
    else:
        bars = alt.Chart(chart_data).mark_bar(
            color=color, opacity=0.96,
            cornerRadiusTopLeft=5, cornerRadiusTopRight=5,
            stroke=color, strokeWidth=0.4,
        ).encode(
            x=alt.X(
                f"{category}:N",
                sort=None,
                title=None,
                axis=alt.Axis(labelFontWeight="bold", labelAngle=-25, labelLimit=150),
            ),
            y=alt.Y(
                f"{value}:Q",
                title=value_title,
                axis=alt.Axis(labelFontWeight="bold", titleFontWeight="bold"),
            ),
            tooltip=[
                alt.Tooltip(f"{category}:N", title=title),
                alt.Tooltip(f"{value}:Q", title=value_title, format=",.2f"),
            ],
        )
        labels = alt.Chart(chart_data).mark_text(
            dy=-8, fontWeight="bold", color="#34445B"
        ).encode(
            x=alt.X(f"{category}:N", sort=None),
            y=alt.Y(f"{value}:Q"),
            text=alt.Text(f"{value}:Q", format=",.2f"),
        )
        chart = (bars + labels).properties(height=height)
    chart = chart.configure_view(strokeOpacity=0, fill="#FBFCFF").configure_axis(
        gridColor="#DCE5F2",
        gridOpacity=0.9,
        domainColor="#AAB8CC",
        tickColor="#AAB8CC",
        labelColor="#334155",
        titleColor="#1E293B",
        labelFontSize=11,
        titleFontSize=12,
    ).configure_title(
        color="#172B4D",
        fontSize=14,
        fontWeight="bold",
        anchor="start",
    )
    st.altair_chart(chart, use_container_width=True)


def metric_table(frame: pd.DataFrame, rename: dict[str, str]) -> None:
    """Show a consistently formatted detail table."""
    display = frame.rename(columns=rename).copy()
    for column in ("Total premium", "Total claims cost", "Average premium"):
        if column in display:
            display[column] = display[column].map(lambda value: f"₹{value:,.2f}")
    if "Total exposure" in display:
        display["Total exposure"] = display["Total exposure"].map(lambda value: f"{value:,.2f}")
    for column in ("Total observations", "Total policies", "Customer records"):
        if column in display:
            display[column] = display[column].map(lambda value: f"{value:,}")
    st.dataframe(display, use_container_width=True, hide_index=True)


def render_overview() -> None:
    summary = load_endpoint("summary")
    yearly = load_endpoint("yearly").get("years", [])
    years = pd.DataFrame(yearly).sort_values("period") if yearly else pd.DataFrame()

    st.subheader("📌 Portfolio overview")
    if not years.empty:
        period = f"{int(years['period'].min())}–{int(years['period'].max())}"
    else:
        period = "Not available"
    render_metric_row([
        ("Total policies", f"{summary['total_policies']:,}", METRIC_HELP["Total policies"]),
        ("Total observations", f"{summary['total_observations']:,}", METRIC_HELP["Total observations"]),
        ("Total premium", format_currency_millions(summary["total_premium"]), METRIC_HELP["Total premium"]),
        ("Total claims cost", format_currency_millions(summary["total_claims_cost"]), METRIC_HELP["Total claims cost"]),
        ("Average premium", f"₹{summary['average_premium']:,.2f}", METRIC_HELP["Average premium"]),
        ("Total exposure", f"{summary['total_exposure']:,.2f}", METRIC_HELP["Total exposure"]),
    ])
    info_heading("🗓️ Reporting period", METRIC_HELP["Period covered"])
    st.markdown(f"**{period}**")

    if years.empty:
        st.info("No yearly performance data is currently available.")
        return

    frame = years.copy()
    frame["period"] = frame["period"].astype(int).astype(str)
    frame["premium_m"] = frame["total_premium"] / 1_000_000
    frame["claims_cost_m"] = frame["total_claims_cost"] / 1_000_000

    st.divider()
    st.subheader("📈 Yearly performance trends")
    info_heading(
        "How to read these charts",
        "Each bar represents one reporting year. Labels above bars show the metric value; hover over a bar for the exact value.",
    )
    a, b, c = st.columns(3)
    with a:
        st.markdown("**💰 Premium**")
        render_bar_chart(frame, "period", "premium_m", "Year", COLORS["blue"], "₹ millions", height=290)
    with b:
        st.markdown("**🧾 Claims cost**")
        render_bar_chart(frame, "period", "claims_cost_m", "Year", COLORS["orange"], "₹ millions", height=290)
    with c:
        st.markdown("**🛡️ Exposure**")
        render_bar_chart(frame, "period", "total_exposure", "Year", COLORS["teal"], "Exposure", height=290)


def render_breakdown_page(
    *,
    endpoint: str,
    response_key: str,
    title: str,
    category_fields: list[str],
    category_labels: dict[str, str],
    chart_category: str,
    chart_title: str,
    chart_metric: str = "total_premium",
) -> None:
    records = load_endpoint(endpoint).get(response_key, [])
    st.subheader(title)
    if not records:
        st.info("No records are currently available for this analysis.")
        return
    frame = pd.DataFrame(records)
    for field in category_fields:
        frame[field] = frame[field].fillna("Not available").astype(str)
    frame["category_label"] = frame[category_fields].agg(" | ".join, axis=1)

    # Distinct policy/customer counts across categories are not additive.
    # Therefore the page shows additive measures and category count only.
    total_observations = int(frame["total_observations"].sum())
    total_premium = float(frame["total_premium"].sum())
    total_claims = float(frame["total_claims_cost"].sum())
    render_metric_row([
        ("Categories", f"{len(frame):,}", "Number of groups returned by this analysis."),
        ("Total observations", f"{total_observations:,}", METRIC_HELP["Total observations"]),
        ("Total premium", format_currency_millions(total_premium), METRIC_HELP["Total premium"]),
        ("Total claims cost", format_currency_millions(total_claims), METRIC_HELP["Total claims cost"]),
    ])

    metric_options = {
        "Premium": ("total_premium", "Premium (₹ millions)", COLORS["blue"], True),
        "Claims cost": ("total_claims_cost", "Claims cost (₹ millions)", COLORS["orange"], True),
        "Average premium": ("average_premium", "Average premium (₹)", COLORS["purple"], False),
        "Exposure": ("total_exposure", "Exposure", COLORS["teal"], False),
        "Observations": ("total_observations", "Observations", COLORS["pink"], False),
    }
    selected_metric = st.selectbox(
        "Compare categories by",
        list(metric_options),
        key=f"{endpoint}_metric",
    )
    metric_field, axis_title, color, in_millions = metric_options[selected_metric]
    chart_frame = frame[["category_label", metric_field]].copy()
    if in_millions:
        chart_frame[metric_field] = chart_frame[metric_field] / 1_000_000
    render_bar_chart(
        chart_frame,
        "category_label",
        metric_field,
        chart_title,
        color,
        axis_title,
        horizontal=True,
        height=max(300, min(620, 48 * len(chart_frame))),
    )

    st.divider()
    info_heading(
        "Detailed breakdown",
        "Values are grouped using the category fields shown in the first column. Policy counts are distinct within each category and should not be added across categories.",
    )
    rename = {
        **category_labels,
        "total_observations": "Total observations",
        "total_customer_records": "Customer records",
        "total_policies": "Total policies",
        "total_premium": "Total premium",
        "total_claims_cost": "Total claims cost",
        "average_premium": "Average premium",
        "total_exposure": "Total exposure",
    }
    metric_table(frame.drop(columns=["category_label"]), rename)


def render_customer_page() -> None:
    records = load_endpoint("customers").get("customers", [])
    st.subheader("👥 Customer analysis")
    if not records:
        st.info("No customer breakdown data is currently available.")
        return
    frame = pd.DataFrame(records)
    frame["gender"] = frame["gender"].fillna("Not available").astype(str)
    render_metric_row([
        ("Customer groups", f"{len(frame):,}", "Number of gender groups returned by the customer analysis."),
        ("Customer records", f"{int(frame['total_customer_records'].sum()):,}", METRIC_HELP["Customer records"]),
        ("Total observations", f"{int(frame['total_observations'].sum()):,}", METRIC_HELP["Total observations"]),
        ("Total premium", format_currency_millions(float(frame["total_premium"].sum())), METRIC_HELP["Total premium"]),
    ])
    a, b = st.columns(2)
    with a:
        st.markdown("**Customer records by gender**")
        render_bar_chart(frame, "gender", "total_customer_records", "Gender", COLORS["purple"], "Customer records")
    with b:
        st.markdown("**Premium by gender**")
        premium = frame.assign(premium_m=frame["total_premium"] / 1_000_000)
        render_bar_chart(premium, "gender", "premium_m", "Gender", COLORS["blue"], "₹ millions")
    metric_table(frame, {
        "gender": "Gender",
        "total_observations": "Total observations",
        "total_customer_records": "Customer records",
        "total_policies": "Total policies",
        "total_premium": "Total premium",
        "total_claims_cost": "Total claims cost",
        "average_premium": "Average premium",
        "total_exposure": "Total exposure",
    })


def render_cohort_line_chart(
    data: pd.DataFrame,
    value: str,
    title: str,
    color: str,
    value_title: str,
    *,
    height: int = 330,
) -> None:
    """Render a clean interactive cohort trend without crowded permanent labels."""
    chart = (
        alt.Chart(data)
        .mark_line(
            color=color,
            strokeWidth=3.5,
            point=alt.OverlayMarkDef(
                filled=True, size=78, color=color, stroke="#FFFFFF", strokeWidth=1.5
            ),
        )
        .encode(
            x=alt.X(
                "cohort_year:Q",
                title="Year insured became effective",
                scale=alt.Scale(zero=False),
                axis=alt.Axis(
                    format="d",
                    tickCount=8,
                    labelFontWeight="bold",
                    titleFontWeight="bold",
                    labelAngle=0,
                ),
            ),
            y=alt.Y(
                f"{value}:Q",
                title=value_title,
                axis=alt.Axis(labelFontWeight="bold", titleFontWeight="bold"),
            ),
            tooltip=[
                alt.Tooltip("cohort_year:Q", title="Effective year", format="d"),
                alt.Tooltip(f"{value}:Q", title=value_title, format=",.2f"),
            ],
        )
        .properties(height=height, title=title)
        .configure_view(strokeOpacity=0, fill="#FBFCFF")
        .configure_axis(
            gridColor="#DCE5F2",
            gridOpacity=0.9,
            domainColor="#AAB8CC",
            tickColor="#AAB8CC",
            labelColor="#334155",
            titleColor="#1E293B",
            labelFontSize=11,
            titleFontSize=12,
        )
        .configure_title(color="#172B4D", fontSize=14, fontWeight="bold", anchor="start")
    )
    st.altair_chart(chart, use_container_width=True)


def render_cohort_page() -> None:
    records = load_endpoint("customer_cohorts").get("customer_cohorts", [])
    st.subheader("🧑‍🤝‍🧑 Customer cohort analysis")
    if not records:
        st.info("No customer cohort data is currently available.")
        return

    frame = pd.DataFrame(records)
    frame["cohort_year"] = pd.to_numeric(
        frame["year_effect_insured"], errors="coerce"
    )
    render_metric_row([
        ("Cohorts", f"{frame['cohort_year'].nunique(dropna=True):,}", "Number of distinct insured-effective-year groups returned by the API. Records without an effective year are retained in the detailed table."),
        ("Customer records", f"{int(frame['total_customer_records'].sum()):,}", METRIC_HELP["Customer records"]),
        ("Total observations", f"{int(frame['total_observations'].sum()):,}", METRIC_HELP["Total observations"]),
        ("Total premium", format_currency_millions(float(frame["total_premium"].sum())), METRIC_HELP["Total premium"]),
    ])
    info_heading(
        "Cohort definition",
        "A cohort groups customer records by YEAR_EFFECT_INSURED, the year insurance became effective for the insured. This is not necessarily the same as the reporting period in the overview.",
    )

    chart_data = frame.dropna(subset=["cohort_year"]).copy()
    if chart_data.empty:
        st.info("No valid insured-effective years are available for charting.")
    else:
        chart_data["cohort_year"] = chart_data["cohort_year"].astype(int)
        min_year = int(chart_data["cohort_year"].min())
        max_year = int(chart_data["cohort_year"].max())

        # Start with a recent 30-year window when possible; the slider can reveal
        # the complete historical range without crowding the initial view.
        default_min = max(min_year, max_year - 29)
        if min_year < max_year:
            selected_range = st.slider(
                "Filter cohort year range",
                min_value=min_year,
                max_value=max_year,
                value=(default_min, max_year),
                step=1,
                help="Adjust the range to explore earlier or later insured-effective-year cohorts.",
                key="cohort_year_range",
            )
            filtered = chart_data[
                chart_data["cohort_year"].between(
                    selected_range[0], selected_range[1]
                )
            ].sort_values("cohort_year")
            st.caption(
                f"Showing cohorts from {selected_range[0]} to {selected_range[1]} "
                f"({len(filtered):,} yearly cohorts). The detailed table below retains the full dataset."
            )
        else:
            filtered = chart_data.sort_values("cohort_year")
            st.caption(f"Showing the available cohort year: {min_year}.")

        premium = filtered.assign(
            premium_m=filtered["total_premium"] / 1_000_000
        )
        a, b = st.columns(2)
        with a:
            st.markdown("**Customer records by effective year**")
            render_cohort_line_chart(
                filtered,
                "total_customer_records",
                "Customer records by effective year",
                COLORS["purple"],
                "Customer records",
            )
        with b:
            st.markdown("**Premium by effective year**")
            render_cohort_line_chart(
                premium,
                "premium_m",
                "Premium by effective year",
                COLORS["blue"],
                "Premium (₹ millions)",
            )

    st.divider()
    info_heading(
        "Complete cohort data",
        "This table includes every cohort year returned by the API, including years outside the selected chart range and records with no effective year.",
    )
    table_frame = frame.copy()
    table_frame["year_effect_insured"] = table_frame["year_effect_insured"].apply(
        lambda value: int(value) if pd.notna(value) else "Not available"
    )
    metric_table(table_frame.drop(columns=["cohort_year"]), {
        "year_effect_insured": "Year insured became effective",
        "total_observations": "Total observations",
        "total_customer_records": "Customer records",
        "total_policies": "Total policies",
        "total_premium": "Total premium",
        "total_claims_cost": "Total claims cost",
        "average_premium": "Average premium",
        "total_exposure": "Total exposure",
    })


st.title("Insurance Risk Intelligence Platform")
st.caption("Portfolio analytics and insurance risk intelligence")

with st.sidebar:
    st.title("📊 Navigation")
    page = st.radio(
        "Dashboard pages",
        list(PAGE_DESCRIPTIONS),
        label_visibility="collapsed",
    )
    st.caption(PAGE_DESCRIPTIONS[page])
    if st.button("🔄 Refresh dashboard", use_container_width=True):
        load_endpoint.clear()
        st.rerun()

try:
    with st.spinner(f"Loading {page.lower()}..."):
        if page == "Portfolio overview":
            render_overview()
        elif page == "Product analysis":
            render_breakdown_page(
                endpoint="products",
                response_key="products",
                title="🧩 Product analysis",
                category_fields=["type_product", "reimbursement"],
                category_labels={"type_product": "Product type", "reimbursement": "Reimbursement"},
                chart_category="category_label",
                chart_title="Product / reimbursement",
            )
        elif page == "Channel analysis":
            render_breakdown_page(
                endpoint="channels",
                response_key="channels",
                title="🏬 Channel analysis",
                category_fields=["distribution_channel"],
                category_labels={"distribution_channel": "Distribution channel"},
                chart_category="category_label",
                chart_title="Distribution channel",
            )
        elif page == "Policy analysis":
            render_breakdown_page(
                endpoint="policies",
                response_key="policies",
                title="📄 Policy analysis",
                category_fields=["type_policy", "type_policy_dg"],
                category_labels={"type_policy": "Policy type", "type_policy_dg": "Policy DG type"},
                chart_category="category_label",
                chart_title="Policy type / DG type",
            )
        elif page == "Customer analysis":
            render_customer_page()
        elif page == "Customer cohort analysis":
            render_cohort_page()

    st.caption("Data source: Gold layer via the authenticated Insurance Risk Intelligence API.")
except DashboardAPIError as exc:
    st.error(f"Unable to load dashboard data: {exc}")
    st.info(
        "Confirm that FastAPI is running and that API_ACCESS_KEY is configured "
        "for this Streamlit process."
    )
except (RuntimeError, KeyError, ValueError) as exc:
    st.error(f"Dashboard configuration or data error: {exc}")
