import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Profitability Analysis",
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

st.title("💰 Profitability Analysis")

st.markdown(
    "Detailed analysis of profit performance, margins, "
    "discounts and loss-making products."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)

average_profit_per_order = (
    total_profit / filtered_df["Order ID"].nunique()
    if filtered_df["Order ID"].nunique() > 0
    else 0
)

loss_orders = (
    filtered_df.loc[
        filtered_df["Profit"] < 0,
        "Order ID"
    ]
    .nunique()
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

with col3:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

with col4:
    st.metric(
        "Avg Profit / Order",
        f"${average_profit_per_order:,.2f}"
    )

with col5:
    st.metric(
        "Loss-Making Orders",
        f"{loss_orders:,}"
    )


# ============================================================
# PROFIT BY CATEGORY
# ============================================================

st.markdown("---")

st.subheader("📦 Profit by Category")

category_profit = (
    filtered_df
    .groupby("Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig_category_profit = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    title="Profit by Category"
)

fig_category_profit.update_layout(
    xaxis_title="Category",
    yaxis_title="Profit"
)

st.plotly_chart(
    fig_category_profit,
    width="stretch"
)


# ============================================================
# PROFIT BY SUB-CATEGORY
# ============================================================

st.subheader("🏷️ Profit by Sub-Category")

subcategory_profit = (
    filtered_df
    .groupby("Sub-Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig_subcategory_profit = px.bar(
    subcategory_profit,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    title="Profit by Sub-Category"
)

fig_subcategory_profit.update_layout(
    xaxis_title="Profit",
    yaxis_title="Sub-Category"
)

st.plotly_chart(
    fig_subcategory_profit,
    width="stretch"
)


# ============================================================
# PROFIT MARGIN BY CATEGORY
# ============================================================

st.markdown("---")

st.subheader("📊 Profit Margin by Category")

category_margin = (
    filtered_df
    .groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_margin["Profit Margin %"] = (
    category_margin["Profit"]
    / category_margin["Sales"]
    * 100
)

category_margin = category_margin.sort_values(
    "Profit Margin %",
    ascending=False
)

fig_category_margin = px.bar(
    category_margin,
    x="Category",
    y="Profit Margin %",
    title="Profit Margin by Category"
)

fig_category_margin.update_layout(
    xaxis_title="Category",
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_category_margin,
    width="stretch"
)


# ============================================================
# MONTHLY PROFIT TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Monthly Profit Trend")

monthly_profit = (
    filtered_df
    .set_index("Order Date")
    .resample("MS")["Profit"]
    .sum()
    .reset_index()
)

fig_monthly_profit = px.line(
    monthly_profit,
    x="Order Date",
    y="Profit",
    markers=True,
    title="Monthly Profit"
)

fig_monthly_profit.update_layout(
    xaxis_title="Month",
    yaxis_title="Profit"
)

st.plotly_chart(
    fig_monthly_profit,
    width="stretch"
)


# ============================================================
# PROFIT BY REGION AND STATE
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("🌎 Profit by Region")

    region_profit = (
        filtered_df
        .groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig_region_profit = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region"
    )

    st.plotly_chart(
        fig_region_profit,
        width="stretch"
    )


with col2:

    st.subheader("📍 Profit by State")

    state_profit = (
        filtered_df
        .groupby(
            "State/Province",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
        .head(15)
    )

    fig_state_profit = px.bar(
        state_profit,
        x="Profit",
        y="State/Province",
        orientation="h",
        title="Top 15 States by Profit"
    )

    st.plotly_chart(
        fig_state_profit,
        width="stretch"
    )


# ============================================================
# DISCOUNT VS PROFIT
# ============================================================

st.markdown("---")

st.subheader("🏷️ Discount vs Profit")

discount_profit = (
    filtered_df[
        [
            "Discount",
            "Profit",
            "Sales",
            "Category"
        ]
    ]
    .copy()
)

fig_discount_profit = px.scatter(
    discount_profit,
    x="Discount",
    y="Profit",
    size="Sales",
    color="Category",
    hover_data=["Sales"],
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
# LOSS-MAKING PRODUCTS
# ============================================================

st.markdown("---")

st.subheader("🔻 Loss-Making Products")

product_profit = (
    filtered_df
    .groupby(
        ["Product ID", "Product Name"],
        as_index=False
    )["Profit"]
    .sum()
    .sort_values(
        "Profit",
        ascending=True
    )
)

loss_products = (
    product_profit[
        product_profit["Profit"] < 0
    ]
    .head(10)
)

if not loss_products.empty:

    fig_loss_products = px.bar(
        loss_products.sort_values("Profit"),
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Loss-Making Products"
    )

    st.plotly_chart(
        fig_loss_products,
        width="stretch"
    )

else:

    st.info(
        "No loss-making products found for the current filters."
    )


# ============================================================
# TOP PROFITABLE PRODUCTS
# ============================================================

st.subheader("🏆 Top Profitable Products")

top_profit_products = (
    product_profit
    .sort_values(
        "Profit",
        ascending=False
    )
    .head(10)
)

fig_top_profit_products = px.bar(
    top_profit_products.sort_values("Profit"),
    x="Profit",
    y="Product Name",
    orientation="h",
    title="Top 10 Most Profitable Products"
)

st.plotly_chart(
    fig_top_profit_products,
    width="stretch"
)


# ============================================================
# PROFITABILITY BY SEGMENT
# ============================================================

st.markdown("---")

st.subheader("👥 Profit by Segment")

segment_profit = (
    filtered_df
    .groupby("Segment", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig_segment_profit = px.bar(
    segment_profit,
    x="Segment",
    y="Profit",
    title="Profit by Segment"
)

st.plotly_chart(
    fig_segment_profit,
    width="stretch"
)


# ============================================================
# DETAILED PROFITABILITY TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Profitability Table")

profit_table = (
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
            "Discount",
            "Profit"
        ]
    ]
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(100)
    .copy()
)

profit_table["Order Date"] = (
    profit_table["Order Date"]
    .dt.strftime("%Y-%m-%d")
)

profit_table["Sales"] = (
    profit_table["Sales"]
    .round(2)
)

profit_table["Discount"] = (
    profit_table["Discount"]
    .round(2)
)

profit_table["Profit"] = (
    profit_table["Profit"]
    .round(2)
)


st.markdown(
    profit_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)

st.caption(
    "Showing the 100 least profitable records from the "
    "currently filtered data."
)


# ============================================================
# CSV DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Profitability Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Profitability Data",
    data=csv_data,
    file_name="profitability_analysis_data.csv",
    mime="text/csv"
)