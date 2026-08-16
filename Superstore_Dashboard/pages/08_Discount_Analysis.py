import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Discount Analysis",
    page_icon="🏷️",
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

st.title("🏷️ Discount Analysis")

st.markdown(
    "Analyze discount patterns and understand their impact "
    "on sales and profitability."
)


# ============================================================
# BASIC CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

average_discount = filtered_df["Discount"].mean()

maximum_discount = filtered_df["Discount"].max()

discounted_records = (
    filtered_df["Discount"] > 0
).sum()

discounted_percentage = (
    discounted_records / len(filtered_df) * 100
    if len(filtered_df) > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Discount KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Average Discount",
        f"{average_discount * 100:.2f}%"
    )

with col2:
    st.metric(
        "Maximum Discount",
        f"{maximum_discount * 100:.0f}%"
    )

with col3:
    st.metric(
        "Discounted Records",
        f"{discounted_records:,}"
    )

with col4:
    st.metric(
        "% Records Discounted",
        f"{discounted_percentage:.2f}%"
    )

with col5:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )


# ============================================================
# DISCOUNT DISTRIBUTION
# ============================================================

st.markdown("---")

st.subheader("📊 Discount Distribution")

discount_distribution = (
    filtered_df
    .groupby("Discount")
    .agg(
        Records=("Discount", "size"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

discount_distribution["Discount %"] = (
    discount_distribution["Discount"] * 100
)

fig_discount_distribution = px.bar(
    discount_distribution,
    x="Discount %",
    y="Records",
    title="Number of Records by Discount Level",
    text_auto=True
)

fig_discount_distribution.update_layout(
    xaxis_title="Discount (%)",
    yaxis_title="Number of Records"
)

st.plotly_chart(
    fig_discount_distribution,
    width="stretch"
)


# ============================================================
# SALES AND PROFIT BY DISCOUNT
# ============================================================

st.markdown("---")

st.subheader("💰 Sales and Profit by Discount Level")

discount_metrics = discount_distribution.copy()

discount_metrics_melted = discount_metrics.melt(
    id_vars="Discount %",
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_discount_metrics = px.bar(
    discount_metrics_melted,
    x="Discount %",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Sales vs Profit by Discount Level"
)

fig_discount_metrics.update_layout(
    xaxis_title="Discount (%)",
    yaxis_title="Amount"
)

st.plotly_chart(
    fig_discount_metrics,
    width="stretch"
)


# ============================================================
# DISCOUNT BY CATEGORY
# ============================================================

st.markdown("---")

st.subheader("📦 Discount by Category")

category_discount = (
    filtered_df
    .groupby("Category")
    .agg(
        Average_Discount=("Discount", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_discount["Average Discount %"] = (
    category_discount["Average_Discount"] * 100
)

fig_category_discount = px.bar(
    category_discount.sort_values(
        "Average Discount %",
        ascending=False
    ),
    x="Category",
    y="Average Discount %",
    title="Average Discount by Category",
    text_auto=".2f"
)

fig_category_discount.update_layout(
    yaxis_title="Average Discount (%)"
)

st.plotly_chart(
    fig_category_discount,
    width="stretch"
)


# ============================================================
# DISCOUNT BY SUB-CATEGORY
# ============================================================

st.subheader("🏷️ Discount by Sub-Category")

subcategory_discount = (
    filtered_df
    .groupby("Sub-Category")
    .agg(
        Average_Discount=("Discount", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

subcategory_discount["Average Discount %"] = (
    subcategory_discount["Average_Discount"] * 100
)

fig_subcategory_discount = px.bar(
    subcategory_discount.sort_values(
        "Average Discount %",
        ascending=False
    ),
    x="Average Discount %",
    y="Sub-Category",
    orientation="h",
    title="Average Discount by Sub-Category"
)

st.plotly_chart(
    fig_subcategory_discount,
    width="stretch"
)


# ============================================================
# DISCOUNT BY REGION
# ============================================================

st.markdown("---")

st.subheader("🌎 Discount by Region")

region_discount = (
    filtered_df
    .groupby("Region")
    .agg(
        Average_Discount=("Discount", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

region_discount["Average Discount %"] = (
    region_discount["Average_Discount"] * 100
)

col1, col2 = st.columns(2)

with col1:

    fig_region_discount = px.bar(
        region_discount.sort_values(
            "Average Discount %",
            ascending=False
        ),
        x="Region",
        y="Average Discount %",
        title="Average Discount by Region",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_region_discount,
        width="stretch"
    )


with col2:

    fig_region_profit = px.bar(
        region_discount.sort_values(
            "Profit",
            ascending=False
        ),
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_region_profit,
        width="stretch"
    )


# ============================================================
# DISCOUNT BY SEGMENT
# ============================================================

st.markdown("---")

st.subheader("👥 Discount by Segment")

segment_discount = (
    filtered_df
    .groupby("Segment")
    .agg(
        Average_Discount=("Discount", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

segment_discount["Average Discount %"] = (
    segment_discount["Average_Discount"] * 100
)

fig_segment_discount = px.bar(
    segment_discount.sort_values(
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
# DISCOUNT VS SALES
# ============================================================

st.markdown("---")

st.subheader("📈 Discount vs Sales")

fig_discount_sales = px.scatter(
    filtered_df,
    x="Discount",
    y="Sales",
    color="Category",
    size="Quantity",
    hover_data=[
        "Order ID",
        "Product Name",
        "Customer Name",
        "Region"
    ],
    title="Discount vs Sales"
)

fig_discount_sales.update_layout(
    xaxis_title="Discount",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_discount_sales,
    width="stretch"
)


# ============================================================
# DISCOUNT VS PROFIT
# ============================================================

st.markdown("---")

st.subheader("⚠️ Discount vs Profit")

fig_discount_profit = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    size="Sales",
    hover_data=[
        "Order ID",
        "Product Name",
        "Customer Name",
        "Region"
    ],
    title="Discount vs Profit"
)

fig_discount_profit.update_layout(
    xaxis_title="Discount",
    yaxis_title="Profit"
)

st.plotly_chart(
    fig_discount_profit,
    width="stretch"
)


# ============================================================
# DISCOUNT VS PROFIT MARGIN
# ============================================================

st.subheader("📊 Discount vs Profit Margin")

discount_margin = filtered_df.copy()

discount_margin["Profit Margin %"] = (
    discount_margin["Profit"]
    / discount_margin["Sales"]
    * 100
)

fig_discount_margin = px.scatter(
    discount_margin,
    x="Discount",
    y="Profit Margin %",
    color="Category",
    size="Sales",
    hover_data=[
        "Order ID",
        "Product Name",
        "Region"
    ],
    title="Discount vs Profit Margin"
)

st.plotly_chart(
    fig_discount_margin,
    width="stretch"
)


# ============================================================
# HIGH-DISCOUNT ORDERS
# ============================================================

st.markdown("---")

st.subheader("🔴 High-Discount Orders")

high_discount_threshold = st.slider(
    "High Discount Threshold (%)",
    min_value=0,
    max_value=80,
    value=30,
    step=5
)

high_discount_orders = filtered_df[
    filtered_df["Discount"]
    >= high_discount_threshold / 100
].copy()

high_discount_summary = (
    high_discount_orders
    .groupby("Order ID")
    .agg(
        Customer=("Customer Name", "first"),
        Region=("Region", "first"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Discount=("Discount", "mean")
    )
    .reset_index()
    .sort_values(
        "Discount",
        ascending=False
    )
    .head(20)
)

high_discount_summary["Discount %"] = (
    high_discount_summary["Discount"] * 100
)

high_discount_summary["Sales"] = (
    high_discount_summary["Sales"].round(2)
)

high_discount_summary["Profit"] = (
    high_discount_summary["Profit"].round(2)
)

high_discount_summary["Discount %"] = (
    high_discount_summary["Discount %"].round(2)
)

st.markdown(
    high_discount_summary[
        [
            "Order ID",
            "Customer",
            "Region",
            "Sales",
            "Profit",
            "Discount %"
        ]
    ].to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# HIGH-DISCOUNT PRODUCTS
# ============================================================

st.markdown("---")

st.subheader("🏷️ Products with Highest Discounts")

product_discount = (
    filtered_df
    .groupby(
        ["Product ID", "Product Name"]
    )
    .agg(
        Average_Discount=("Discount", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
    .sort_values(
        "Average_Discount",
        ascending=False
    )
    .head(15)
)

product_discount["Average Discount %"] = (
    product_discount["Average_Discount"] * 100
)

fig_product_discount = px.bar(
    product_discount.sort_values(
        "Average Discount %"
    ),
    x="Average Discount %",
    y="Product Name",
    orientation="h",
    title="Top 15 Products by Average Discount"
)

st.plotly_chart(
    fig_product_discount,
    width="stretch"
)


# ============================================================
# DISCOUNT IMPACT ON PROFITABILITY
# ============================================================

st.markdown("---")

st.subheader("💡 Discount Impact on Profitability")

profit_impact = (
    filtered_df
    .assign(
        Discount_Band=lambda x: pd.cut(
            x["Discount"],
            bins=[
                -0.01,
                0,
                0.10,
                0.20,
                0.30,
                0.50,
                1.00
            ],
            labels=[
                "No Discount",
                "1–10%",
                "11–20%",
                "21–30%",
                "31–50%",
                "50%+"
            ]
        )
    )
    .groupby(
        "Discount_Band",
        observed=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

profit_impact["Profit Margin %"] = (
    profit_impact["Profit"]
    / profit_impact["Sales"]
    * 100
)

fig_profit_impact = px.bar(
    profit_impact,
    x="Discount_Band",
    y="Profit Margin %",
    title="Profit Margin by Discount Band",
    text_auto=".2f"
)

fig_profit_impact.update_layout(
    xaxis_title="Discount Band",
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_profit_impact,
    width="stretch"
)


# ============================================================
# DETAILED DISCOUNT TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Discount Data")

discount_table = filtered_df[
    [
        "Order ID",
        "Order Date",
        "Customer Name",
        "Region",
        "Category",
        "Sub-Category",
        "Product Name",
        "Sales",
        "Discount",
        "Profit"
    ]
].copy()

discount_table = discount_table.sort_values(
    "Discount",
    ascending=False
)

discount_table["Order Date"] = (
    pd.to_datetime(
        discount_table["Order Date"]
    ).dt.strftime("%Y-%m-%d")
)

discount_table["Discount %"] = (
    discount_table["Discount"] * 100
)

discount_table["Sales"] = (
    discount_table["Sales"].round(2)
)

discount_table["Profit"] = (
    discount_table["Profit"].round(2)
)

discount_table["Discount %"] = (
    discount_table["Discount %"].round(2)
)

st.markdown(
    discount_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Discount Data")

csv_data = discount_table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Discount Analysis",
    data=csv_data,
    file_name="discount_analysis.csv",
    mime="text/csv"
)