import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Order Analysis",
    page_icon="🧾",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = "data/sample_-_superstore.csv"

df = load_data(DATA_FILE)

filtered_df = apply_filters(df)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🧾 Order Analysis")

st.markdown(
    "Analyze order volume, order value, quantity and profitability "
    "across time, regions, categories and customer segments."
)


# ============================================================
# ORDER-LEVEL DATA
# ============================================================

order_summary = (
    filtered_df
    .groupby("Order ID")
    .agg(
        Order_Date=("Order Date", "min"),
        Customer=("Customer Name", "first"),
        Region=("Region", "first"),
        Segment=("Segment", "first"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = order_summary["Order ID"].nunique()

total_sales = order_summary["Sales"].sum()

total_profit = order_summary["Profit"].sum()

total_quantity = order_summary["Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

average_quantity_per_order = (
    total_quantity / total_orders
    if total_orders > 0
    else 0
)

average_profit_per_order = (
    total_profit / total_orders
    if total_orders > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Order KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col2:
    st.metric(
        "Average Order Value",
        f"${average_order_value:,.2f}"
    )

with col3:
    st.metric(
        "Avg Quantity / Order",
        f"{average_quantity_per_order:,.2f}"
    )

with col4:
    st.metric(
        "Avg Profit / Order",
        f"${average_profit_per_order:,.2f}"
    )


# ============================================================
# ORDERS BY MONTH
# ============================================================

st.markdown("---")

st.subheader("📅 Orders by Month")

monthly_orders = (
    order_summary
    .set_index("Order_Date")
    .resample("MS")
    .size()
    .reset_index(name="Orders")
)

fig_monthly_orders = px.line(
    monthly_orders,
    x="Order_Date",
    y="Orders",
    markers=True,
    title="Monthly Order Trend"
)

fig_monthly_orders.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Orders"
)

st.plotly_chart(
    fig_monthly_orders,
    width="stretch"
)


# ============================================================
# ORDERS BY REGION
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌎 Orders by Region")

    region_orders = (
        order_summary
        .groupby("Region", as_index=False)
        .agg(
            Orders=("Order ID", "nunique")
        )
        .sort_values(
            "Orders",
            ascending=False
        )
    )

    fig_region_orders = px.bar(
        region_orders,
        x="Region",
        y="Orders",
        title="Orders by Region",
        text_auto=True
    )

    st.plotly_chart(
        fig_region_orders,
        width="stretch"
    )


# ============================================================
# ORDERS BY CATEGORY
# ============================================================

with col2:

    st.subheader("📦 Orders by Category")

    category_orders = (
        filtered_df
        .groupby("Category")["Order ID"]
        .nunique()
        .reset_index(name="Orders")
        .sort_values(
            "Orders",
            ascending=False
        )
    )

    fig_category_orders = px.bar(
        category_orders,
        x="Category",
        y="Orders",
        title="Orders by Category",
        text_auto=True
    )

    st.plotly_chart(
        fig_category_orders,
        width="stretch"
    )


# ============================================================
# ORDERS BY SEGMENT
# ============================================================

st.markdown("---")

st.subheader("👥 Orders by Segment")

segment_orders = (
    filtered_df
    .groupby("Segment")["Order ID"]
    .nunique()
    .reset_index(name="Orders")
    .sort_values(
        "Orders",
        ascending=False
    )
)

fig_segment_orders = px.bar(
    segment_orders,
    x="Segment",
    y="Orders",
    title="Orders by Segment",
    text_auto=True
)

st.plotly_chart(
    fig_segment_orders,
    width="stretch"
)


# ============================================================
# ORDER VALUE DISTRIBUTION
# ============================================================

st.markdown("---")

st.subheader("💰 Order Value Distribution")

fig_order_value = px.histogram(
    order_summary,
    x="Sales",
    nbins=40,
    title="Distribution of Order Values"
)

fig_order_value.update_layout(
    xaxis_title="Order Value",
    yaxis_title="Number of Orders"
)

st.plotly_chart(
    fig_order_value,
    width="stretch"
)


# ============================================================
# ORDER VALUE BY REGION
# ============================================================

st.markdown("---")

st.subheader("🌎 Order Value by Region")

fig_region_value = px.box(
    order_summary,
    x="Region",
    y="Sales",
    title="Order Value Distribution by Region"
)

fig_region_value.update_layout(
    xaxis_title="Region",
    yaxis_title="Order Value"
)

st.plotly_chart(
    fig_region_value,
    width="stretch"
)


# ============================================================
# ORDER VALUE BY SEGMENT
# ============================================================

st.subheader("👥 Order Value by Segment")

fig_segment_value = px.box(
    order_summary,
    x="Segment",
    y="Sales",
    title="Order Value Distribution by Segment"
)

fig_segment_value.update_layout(
    xaxis_title="Segment",
    yaxis_title="Order Value"
)

st.plotly_chart(
    fig_segment_value,
    width="stretch"
)


# ============================================================
# ORDERS BY QUANTITY RANGE
# ============================================================

st.markdown("---")

st.subheader("📦 Orders by Quantity Range")

quantity_bins = [
    0,
    2,
    5,
    10,
    20,
    float("inf")
]

quantity_labels = [
    "1–2",
    "3–5",
    "6–10",
    "11–20",
    "20+"
]

order_summary["Quantity Range"] = pd.cut(
    order_summary["Quantity"],
    bins=quantity_bins,
    labels=quantity_labels,
    include_lowest=True
)

quantity_range = (
    order_summary
    .groupby(
        "Quantity Range",
        observed=False
    )
    .size()
    .reset_index(name="Orders")
)

fig_quantity_range = px.bar(
    quantity_range,
    x="Quantity Range",
    y="Orders",
    title="Orders by Quantity Range",
    text_auto=True
)

st.plotly_chart(
    fig_quantity_range,
    width="stretch"
)


# ============================================================
# PROFITABLE VS LOSS-MAKING ORDERS
# ============================================================

st.markdown("---")

st.subheader("📈 Profitable vs Loss-Making Orders")

order_summary["Order Type"] = order_summary[
    "Profit"
].apply(
    lambda x: "Profitable"
    if x >= 0
    else "Loss-Making"
)

order_type = (
    order_summary
    .groupby("Order Type")
    .size()
    .reset_index(name="Orders")
)

fig_order_type = px.pie(
    order_type,
    names="Order Type",
    values="Orders",
    title="Profitable vs Loss-Making Orders"
)

st.plotly_chart(
    fig_order_type,
    width="stretch"
)


# ============================================================
# ORDER TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Order Table")

order_table = order_summary[
    [
        "Order ID",
        "Order_Date",
        "Customer",
        "Region",
        "Segment",
        "Sales",
        "Profit",
        "Quantity"
    ]
].copy()

order_table = order_table.sort_values(
    "Sales",
    ascending=False
)

order_table["Order_Date"] = (
    order_table["Order_Date"]
    .dt.strftime("%Y-%m-%d")
)

order_table["Sales"] = (
    order_table["Sales"]
    .round(2)
)

order_table["Profit"] = (
    order_table["Profit"]
    .round(2)
)

order_table["Quantity"] = (
    order_table["Quantity"]
    .astype(int)
)

# Use HTML instead of st.dataframe()
# because PyArrow is blocked by the Windows
# Application Control policy on this machine.

st.markdown(
    order_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD ORDER DATA
# ============================================================

st.markdown("---")

st.subheader("📥 Download Order Data")

csv_data = order_table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Order Analysis",
    data=csv_data,
    file_name="order_analysis.csv",
    mime="text/csv"
)