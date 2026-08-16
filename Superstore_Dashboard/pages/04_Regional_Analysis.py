import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Regional Analysis",
    page_icon="🌎",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = "data/sample_-_superstore.csv"

df = load_data(DATA_FILE)


# ============================================================
# APPLY COMMON FILTERS
# ============================================================

filtered_df = apply_filters(df)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🌎 Regional Analysis")

st.markdown(
    "Compare sales and profitability performance across "
    "Central, East, South and West regions."
)


# ============================================================
# REGION SUMMARY
# ============================================================

region_summary = (
    filtered_df
    .groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Customers=("Customer ID", "nunique")
    )
    .reset_index()
)

region_summary["Profit Margin %"] = (
    region_summary["Profit"]
    / region_summary["Sales"]
    * 100
)


# ============================================================
# REGION KPI CARDS
# ============================================================

st.subheader("📊 Regional Performance")

regions = ["Central", "East", "South", "West"]

cols = st.columns(4)

for col, region in zip(cols, regions):

    region_data = region_summary[
        region_summary["Region"] == region
    ]

    with col:

        if not region_data.empty:

            sales = region_data["Sales"].iloc[0]
            profit = region_data["Profit"].iloc[0]
            margin = region_data["Profit Margin %"].iloc[0]

            st.metric(
                region,
                f"${sales:,.0f}",
                f"Profit ${profit:,.0f}"
            )

            st.caption(
                f"Profit Margin: {margin:.2f}%"
            )

        else:

            st.metric(
                region,
                "$0",
                "No data"
            )


# ============================================================
# REGIONAL SUMMARY TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Regional Summary")

display_summary = region_summary.copy()

display_summary["Sales"] = (
    display_summary["Sales"].round(2)
)

display_summary["Profit"] = (
    display_summary["Profit"].round(2)
)

display_summary["Profit Margin %"] = (
    display_summary["Profit Margin %"].round(2)
)

display_summary = display_summary[
    [
        "Region",
        "Sales",
        "Profit",
        "Orders",
        "Quantity",
        "Customers",
        "Profit Margin %"
    ]
]

st.markdown(
    display_summary.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# SALES BY REGION
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("💰 Sales by Region")

    fig_sales_region = px.bar(
        region_summary.sort_values(
            "Sales",
            ascending=False
        ),
        x="Region",
        y="Sales",
        title="Sales by Region",
        text_auto=".2s"
    )

    fig_sales_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_sales_region,
        width="stretch"
    )


# ============================================================
# PROFIT BY REGION
# ============================================================

with col2:

    st.subheader("📈 Profit by Region")

    fig_profit_region = px.bar(
        region_summary.sort_values(
            "Profit",
            ascending=False
        ),
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s"
    )

    fig_profit_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_profit_region,
        width="stretch"
    )


# ============================================================
# PROFIT MARGIN BY REGION
# ============================================================

st.markdown("---")

st.subheader("📊 Profit Margin by Region")

fig_margin_region = px.bar(
    region_summary.sort_values(
        "Profit Margin %",
        ascending=False
    ),
    x="Region",
    y="Profit Margin %",
    title="Profit Margin by Region",
    text_auto=".2f"
)

fig_margin_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_margin_region,
    width="stretch"
)


# ============================================================
# REGIONAL SALES VS PROFIT
# ============================================================

st.markdown("---")

st.subheader("⚖️ Sales vs Profit by Region")

sales_profit_region = region_summary.melt(
    id_vars="Region",
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_sales_profit = px.bar(
    sales_profit_region,
    x="Region",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Sales vs Profit by Region"
)

fig_sales_profit.update_layout(
    xaxis_title="Region",
    yaxis_title="Amount"
)

st.plotly_chart(
    fig_sales_profit,
    width="stretch"
)


# ============================================================
# ORDERS AND QUANTITY BY REGION
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("🧾 Orders by Region")

    fig_orders = px.bar(
        region_summary.sort_values(
            "Orders",
            ascending=False
        ),
        x="Region",
        y="Orders",
        title="Orders by Region",
        text_auto=True
    )

    st.plotly_chart(
        fig_orders,
        width="stretch"
    )


with col2:

    st.subheader("📦 Quantity by Region")

    fig_quantity = px.bar(
        region_summary.sort_values(
            "Quantity",
            ascending=False
        ),
        x="Region",
        y="Quantity",
        title="Quantity Sold by Region",
        text_auto=True
    )

    st.plotly_chart(
        fig_quantity,
        width="stretch"
    )


# ============================================================
# CUSTOMERS BY REGION
# ============================================================

st.markdown("---")

st.subheader("👥 Customers by Region")

fig_customers = px.bar(
    region_summary.sort_values(
        "Customers",
        ascending=False
    ),
    x="Region",
    y="Customers",
    title="Unique Customers by Region",
    text_auto=True
)

st.plotly_chart(
    fig_customers,
    width="stretch"
)


# ============================================================
# REGION × CATEGORY
# ============================================================

st.markdown("---")

st.subheader("🗂️ Sales by Region and Category")

region_category = (
    filtered_df
    .groupby(
        ["Region", "Category"],
        as_index=False
    )["Sales"]
    .sum()
)

fig_region_category = px.bar(
    region_category,
    x="Region",
    y="Sales",
    color="Category",
    barmode="group",
    title="Sales by Region and Category"
)

st.plotly_chart(
    fig_region_category,
    width="stretch"
)


# ============================================================
# REGION × SUB-CATEGORY
# ============================================================

st.subheader("🏷️ Profit by Region and Sub-Category")

region_subcategory = (
    filtered_df
    .groupby(
        ["Region", "Sub-Category"],
        as_index=False
    )["Profit"]
    .sum()
)

fig_region_subcategory = px.bar(
    region_subcategory,
    x="Region",
    y="Profit",
    color="Sub-Category",
    title="Profit by Region and Sub-Category"
)

st.plotly_chart(
    fig_region_subcategory,
    width="stretch"
)


# ============================================================
# STATE PERFORMANCE
# ============================================================

st.markdown("---")

st.subheader("📍 State Performance by Region")

state_region = (
    filtered_df
    .groupby(
        ["Region", "State/Province"],
        as_index=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

selected_region = st.selectbox(
    "Select Region",
    regions
)

selected_states = state_region[
    state_region["Region"] == selected_region
].sort_values(
    "Sales",
    ascending=False
)

fig_states = px.bar(
    selected_states.head(15),
    x="Sales",
    y="State/Province",
    orientation="h",
    title=f"Top 15 States by Sales — {selected_region}"
)

st.plotly_chart(
    fig_states,
    width="stretch"
)


# ============================================================
# REGIONAL PERFORMANCE TABLE
# ============================================================

st.markdown("---")

st.subheader("📑 Detailed Regional Performance")

detailed_region = region_summary.copy()

detailed_region["Sales"] = (
    detailed_region["Sales"].round(2)
)

detailed_region["Profit"] = (
    detailed_region["Profit"].round(2)
)

detailed_region["Profit Margin %"] = (
    detailed_region["Profit Margin %"].round(2)
)

st.markdown(
    detailed_region.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Regional Analysis")

csv_data = region_summary.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Regional Summary",
    data=csv_data,
    file_name="regional_analysis.csv",
    mime="text/csv"
)