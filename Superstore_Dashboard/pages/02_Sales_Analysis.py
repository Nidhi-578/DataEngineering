import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Analysis",
    page_icon="💰",
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

st.title("💰 Sales Analysis")

st.markdown(
    "Detailed analysis of sales performance across time, "
    "categories, regions, states and products."
)


# ============================================================
# KPI SECTION
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_quantity = filtered_df["Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "Total Quantity",
        f"{total_quantity:,}"
    )

with col4:
    st.metric(
        "Average Order Value",
        f"${average_order_value:,.2f}"
    )


# ============================================================
# MONTHLY SALES TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .set_index("Order Date")
    .resample("MS")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)


# ============================================================
# QUARTERLY SALES TREND
# ============================================================

st.markdown("---")

st.subheader("📊 Quarterly Sales Trend")

quarterly_sales = (
    filtered_df
    .set_index("Order Date")
    .resample("QS")["Sales"]
    .sum()
    .reset_index()
)

quarterly_sales["Quarter"] = (
    quarterly_sales["Order Date"]
    .dt.to_period("Q")
    .astype(str)
)

fig_quarterly = px.bar(
    quarterly_sales,
    x="Quarter",
    y="Sales",
    title="Quarterly Sales"
)

fig_quarterly.update_layout(
    xaxis_title="Quarter",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_quarterly,
    width="stretch"
)


# ============================================================
# YEAR-OVER-YEAR SALES COMPARISON
# ============================================================

st.markdown("---")

st.subheader("📅 Year-over-Year Sales Comparison")

yearly_sales = (
    filtered_df
    .groupby(
        filtered_df["Order Date"].dt.year
    )["Sales"]
    .sum()
    .reset_index()
)

yearly_sales.columns = ["Year", "Sales"]

yearly_sales["YoY Growth %"] = (
    yearly_sales["Sales"]
    .pct_change()
    .fillna(0)
    * 100
)


col1, col2 = st.columns(2)

with col1:

    fig_yoy = px.bar(
        yearly_sales,
        x="Year",
        y="Sales",
        title="Sales by Year"
    )

    st.plotly_chart(
        fig_yoy,
        width="stretch"
    )


with col2:

    fig_growth = px.bar(
        yearly_sales,
        x="Year",
        y="YoY Growth %",
        title="Year-over-Year Sales Growth"
    )

    st.plotly_chart(
        fig_growth,
        width="stretch"
    )


# ============================================================
# CATEGORY SALES
# ============================================================

st.markdown("---")

st.subheader("📦 Sales by Category")

category_sales = (
    filtered_df
    .groupby(
        "Category",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category"
)

st.plotly_chart(
    fig_category,
    width="stretch"
)


# ============================================================
# SUB-CATEGORY SALES
# ============================================================

st.subheader("🏷️ Sales by Sub-Category")

subcategory_sales = (
    filtered_df
    .groupby(
        "Sub-Category",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)

fig_subcategory = px.bar(
    subcategory_sales,
    x="Sub-Category",
    y="Sales",
    title="Sales by Sub-Category"
)

st.plotly_chart(
    fig_subcategory,
    width="stretch"
)


# ============================================================
# REGION AND STATE SALES
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("🌎 Sales by Region")

    region_sales = (
        filtered_df
        .groupby(
            "Region",
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig_region,
        width="stretch"
    )


with col2:

    st.subheader("📍 Sales by State")

    state_sales = (
        filtered_df
        .groupby(
            "State/Province",
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(15)
    )

    fig_state = px.bar(
        state_sales,
        x="Sales",
        y="State/Province",
        orientation="h",
        title="Top 15 States by Sales"
    )

    st.plotly_chart(
        fig_state,
        width="stretch"
    )


# ============================================================
# TOP AND BOTTOM PRODUCTS
# ============================================================

st.markdown("---")

st.subheader("🏆 Top & Bottom Products")

product_sales = (
    filtered_df
    .groupby(
        ["Product ID", "Product Name"],
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)

top_products = product_sales.head(10)

bottom_products = (
    product_sales
    .sort_values(
        "Sales",
        ascending=True
    )
    .head(10)
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### 🥇 Top 10 Products")

    fig_top_products = px.bar(
        top_products.sort_values("Sales"),
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales"
    )

    st.plotly_chart(
        fig_top_products,
        width="stretch"
    )


with col2:

    st.markdown("### 📉 Bottom 10 Products")

    fig_bottom_products = px.bar(
        bottom_products.sort_values("Sales"),
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Bottom 10 Products by Sales"
    )

    st.plotly_chart(
        fig_bottom_products,
        width="stretch"
    )


# ============================================================
# DETAILED SALES TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Sales Table")

table_data = (
    filtered_df[
        [
            "Order ID",
            "Order Date",
            "Customer Name",
            "Region",
            "Category",
            "Sub-Category",
            "Product Name",
            "Sales",
            "Quantity",
            "Discount",
            "Profit"
        ]
    ]
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(100)
    .copy()
)

table_data["Order Date"] = (
    table_data["Order Date"]
    .dt.strftime("%Y-%m-%d")
)

table_data["Sales"] = table_data["Sales"].round(2)

table_data["Discount"] = table_data["Discount"].round(2)

table_data["Profit"] = table_data["Profit"].round(2)


st.markdown(
    table_data.to_html(
        index=False,
        classes="sales-table",
        border=0
    ),
    unsafe_allow_html=True
)

st.caption(
    "Showing the top 100 records by Sales from the currently filtered data."
)


# ============================================================
# CSV DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Sales Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data",
    data=csv_data,
    file_name="sales_analysis_data.csv",
    mime="text/csv"
)