import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer & Segment Analysis",
    page_icon="👥",
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

st.title("👥 Customer & Segment Analysis")

st.markdown(
    "Analyze customer contribution and compare performance "
    "across Consumer, Corporate and Home Office segments."
)


# ============================================================
# CUSTOMER-LEVEL SUMMARY
# ============================================================

customer_summary = (
    filtered_df
    .groupby("Customer Name")
    .agg(
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)


# ============================================================
# CUSTOMER KPIs
# ============================================================

total_customers = customer_summary["Customer Name"].nunique()

average_sales_customer = (
    customer_summary["Sales"].mean()
    if total_customers > 0
    else 0
)

average_profit_customer = (
    customer_summary["Profit"].mean()
    if total_customers > 0
    else 0
)

top_customer = (
    customer_summary
    .sort_values("Sales", ascending=False)
    .iloc[0]["Customer Name"]
    if total_customers > 0
    else "N/A"
)


# ============================================================
# CUSTOMER KPI CARDS
# ============================================================

st.subheader("👤 Customer Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Avg Sales / Customer",
        f"${average_sales_customer:,.2f}"
    )

with col3:
    st.metric(
        "Avg Profit / Customer",
        f"${average_profit_customer:,.2f}"
    )

with col4:
    st.metric(
        "Top Customer",
        top_customer
    )


# ============================================================
# TOP CUSTOMERS BY SALES
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("🏆 Top 10 Customers by Sales")

    top_sales_customers = (
        customer_summary
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )

    fig_top_sales = px.bar(
        top_sales_customers.sort_values("Sales"),
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Top 10 Customers by Sales"
    )

    st.plotly_chart(
        fig_top_sales,
        width="stretch"
    )


# ============================================================
# TOP CUSTOMERS BY PROFIT
# ============================================================

with col2:

    st.subheader("💰 Top 10 Customers by Profit")

    top_profit_customers = (
        customer_summary
        .sort_values(
            "Profit",
            ascending=False
        )
        .head(10)
    )

    fig_top_profit = px.bar(
        top_profit_customers.sort_values("Profit"),
        x="Profit",
        y="Customer Name",
        orientation="h",
        title="Top 10 Customers by Profit"
    )

    st.plotly_chart(
        fig_top_profit,
        width="stretch"
    )


# ============================================================
# CUSTOMER ORDER FREQUENCY
# ============================================================

st.markdown("---")

st.subheader("🔄 Customer Order Frequency")

order_frequency = (
    customer_summary
    .groupby("Orders")
    .size()
    .reset_index(name="Customers")
)

fig_frequency = px.bar(
    order_frequency,
    x="Orders",
    y="Customers",
    title="Number of Customers by Order Frequency"
)

fig_frequency.update_layout(
    xaxis_title="Number of Orders",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig_frequency,
    width="stretch"
)


# ============================================================
# CUSTOMER SALES & PROFIT DISTRIBUTION
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📊 Customer Sales Distribution")

    fig_sales_distribution = px.histogram(
        customer_summary,
        x="Sales",
        nbins=30,
        title="Customer Sales Distribution"
    )

    st.plotly_chart(
        fig_sales_distribution,
        width="stretch"
    )


with col2:

    st.subheader("📈 Customer Profit Distribution")

    fig_profit_distribution = px.histogram(
        customer_summary,
        x="Profit",
        nbins=30,
        title="Customer Profit Distribution"
    )

    st.plotly_chart(
        fig_profit_distribution,
        width="stretch"
    )


# ============================================================
# CUSTOMER TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Customer Performance Table")

customer_table = (
    customer_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .copy()
)

customer_table["Sales"] = (
    customer_table["Sales"]
    .round(2)
)

customer_table["Profit"] = (
    customer_table["Profit"]
    .round(2)
)

st.markdown(
    customer_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# SEGMENT SUMMARY
# ============================================================

st.markdown("---")

st.subheader("🏢 Segment Performance")

segment_summary = (
    filtered_df
    .groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Customers=("Customer ID", "nunique"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Average_Discount=("Discount", "mean")
    )
    .reset_index()
)

segment_summary["Profit Margin %"] = (
    segment_summary["Profit"]
    / segment_summary["Sales"]
    * 100
)

segment_summary["Average Discount %"] = (
    segment_summary["Average_Discount"]
    * 100
)


# ============================================================
# SEGMENT KPI CARDS
# ============================================================

segments = [
    "Consumer",
    "Corporate",
    "Home Office"
]

cols = st.columns(3)

for col, segment in zip(cols, segments):

    segment_data = segment_summary[
        segment_summary["Segment"] == segment
    ]

    with col:

        if not segment_data.empty:

            sales = segment_data["Sales"].iloc[0]
            profit = segment_data["Profit"].iloc[0]
            customers = segment_data["Customers"].iloc[0]

            st.metric(
                segment,
                f"${sales:,.0f}",
                f"Profit ${profit:,.0f}"
            )

            st.caption(
                f"Customers: {customers:,}"
            )

        else:

            st.metric(
                segment,
                "$0"
            )


# ============================================================
# SEGMENT SUMMARY TABLE
# ============================================================

st.markdown("---")

display_segment = segment_summary[
    [
        "Segment",
        "Sales",
        "Profit",
        "Customers",
        "Orders",
        "Quantity",
        "Profit Margin %",
        "Average Discount %"
    ]
].copy()

display_segment["Sales"] = (
    display_segment["Sales"].round(2)
)

display_segment["Profit"] = (
    display_segment["Profit"].round(2)
)

display_segment["Profit Margin %"] = (
    display_segment["Profit Margin %"].round(2)
)

display_segment["Average Discount %"] = (
    display_segment["Average Discount %"].round(2)
)

st.markdown(
    display_segment.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# SALES BY SEGMENT
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("💰 Sales by Segment")

    fig_segment_sales = px.bar(
        segment_summary.sort_values(
            "Sales",
            ascending=False
        ),
        x="Segment",
        y="Sales",
        title="Sales by Segment",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_segment_sales,
        width="stretch"
    )


# ============================================================
# PROFIT BY SEGMENT
# ============================================================

with col2:

    st.subheader("📈 Profit by Segment")

    fig_segment_profit = px.bar(
        segment_summary.sort_values(
            "Profit",
            ascending=False
        ),
        x="Segment",
        y="Profit",
        title="Profit by Segment",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_segment_profit,
        width="stretch"
    )


# ============================================================
# QUANTITY BY SEGMENT
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("📦 Quantity by Segment")

    fig_segment_quantity = px.bar(
        segment_summary.sort_values(
            "Quantity",
            ascending=False
        ),
        x="Segment",
        y="Quantity",
        title="Quantity by Segment",
        text_auto=True
    )

    st.plotly_chart(
        fig_segment_quantity,
        width="stretch"
    )


# ============================================================
# ORDERS BY SEGMENT
# ============================================================

with col2:

    st.subheader("🧾 Orders by Segment")

    fig_segment_orders = px.bar(
        segment_summary.sort_values(
            "Orders",
            ascending=False
        ),
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
# PROFIT MARGIN BY SEGMENT
# ============================================================

st.markdown("---")

st.subheader("📊 Profit Margin by Segment")

fig_segment_margin = px.bar(
    segment_summary.sort_values(
        "Profit Margin %",
        ascending=False
    ),
    x="Segment",
    y="Profit Margin %",
    title="Profit Margin by Segment",
    text_auto=".2f"
)

fig_segment_margin.update_layout(
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_segment_margin,
    width="stretch"
)


# ============================================================
# DISCOUNT BY SEGMENT
# ============================================================

st.subheader("🏷️ Average Discount by Segment")

fig_segment_discount = px.bar(
    segment_summary.sort_values(
        "Average Discount %",
        ascending=False
    ),
    x="Segment",
    y="Average Discount %",
    title="Average Discount by Segment",
    text_auto=".2f"
)

fig_segment_discount.update_layout(
    yaxis_title="Average Discount (%)"
)

st.plotly_chart(
    fig_segment_discount,
    width="stretch"
)


# ============================================================
# SEGMENT SALES VS PROFIT
# ============================================================

st.markdown("---")

st.subheader("⚖️ Sales vs Profit by Segment")

segment_comparison = segment_summary.melt(
    id_vars="Segment",
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_segment_comparison = px.bar(
    segment_comparison,
    x="Segment",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Sales vs Profit by Segment"
)

st.plotly_chart(
    fig_segment_comparison,
    width="stretch"
)


# ============================================================
# DOWNLOAD CUSTOMER DATA
# ============================================================

st.markdown("---")

st.subheader("📥 Download Customer & Segment Data")

customer_csv = customer_summary.to_csv(
    index=False
).encode("utf-8")

segment_csv = segment_summary.to_csv(
    index=False
).encode("utf-8")


col1, col2 = st.columns(2)

with col1:

    st.download_button(
        label="Download Customer Summary",
        data=customer_csv,
        file_name="customer_summary.csv",
        mime="text/csv"
    )

with col2:

    st.download_button(
        label="Download Segment Summary",
        data=segment_csv,
        file_name="segment_summary.csv",
        mime="text/csv"
    )