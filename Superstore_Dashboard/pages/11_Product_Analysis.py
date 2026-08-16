import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
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

st.title("📦 Product Analysis")

st.markdown(
    "Analyze product sales, profitability, quantity, discounts "
    "and performance across categories and sub-categories."
)


# ============================================================
# PRODUCT SUMMARY
# ============================================================

product_summary = (
    filtered_df
    .groupby(
        ["Product ID", "Product Name", "Category", "Sub-Category"],
        as_index=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique"),
        Average_Discount=("Discount", "mean")
    )
)

product_summary["Profit Margin %"] = (
    product_summary["Profit"]
    / product_summary["Sales"]
    * 100
)

product_summary["Average Discount %"] = (
    product_summary["Average_Discount"]
    * 100
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_products = product_summary["Product ID"].nunique()

total_sales = product_summary["Sales"].sum()

total_profit = product_summary["Profit"].sum()

total_quantity = product_summary["Quantity"].sum()

average_product_sales = (
    product_summary["Sales"].mean()
    if total_products > 0
    else 0
)

average_product_profit = (
    product_summary["Profit"].mean()
    if total_products > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Product KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Products",
        f"{total_products:,}"
    )

with col2:
    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

with col3:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )

with col4:
    st.metric(
        "Total Quantity",
        f"{total_quantity:,}"
    )

with col5:
    st.metric(
        "Avg Sales / Product",
        f"${average_product_sales:,.2f}"
    )


# ============================================================
# TOP PRODUCTS BY SALES
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top 10 Products by Sales")

    top_sales = (
        product_summary
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )

    fig_top_sales = px.bar(
        top_sales.sort_values("Sales"),
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales"
    )

    st.plotly_chart(
        fig_top_sales,
        width="stretch"
    )


# ============================================================
# TOP PRODUCTS BY PROFIT
# ============================================================

with col2:

    st.subheader("💰 Top 10 Products by Profit")

    top_profit = (
        product_summary
        .sort_values(
            "Profit",
            ascending=False
        )
        .head(10)
    )

    fig_top_profit = px.bar(
        top_profit.sort_values("Profit"),
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Profit"
    )

    st.plotly_chart(
        fig_top_profit,
        width="stretch"
    )


# ============================================================
# BOTTOM PRODUCTS BY PROFIT
# ============================================================

st.markdown("---")

st.subheader("🔻 Bottom 10 Products by Profit")

bottom_profit = (
    product_summary
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(10)
)

fig_bottom_profit = px.bar(
    bottom_profit.sort_values("Profit"),
    x="Profit",
    y="Product Name",
    orientation="h",
    title="Bottom 10 Products by Profit"
)

st.plotly_chart(
    fig_bottom_profit,
    width="stretch"
)


# ============================================================
# TOP PRODUCTS BY QUANTITY
# ============================================================

st.markdown("---")

st.subheader("📦 Top 10 Products by Quantity")

top_quantity = (
    product_summary
    .sort_values(
        "Quantity",
        ascending=False
    )
    .head(10)
)

fig_top_quantity = px.bar(
    top_quantity.sort_values("Quantity"),
    x="Quantity",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Quantity"
)

st.plotly_chart(
    fig_top_quantity,
    width="stretch"
)


# ============================================================
# CATEGORY SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📂 Category Performance")

category_summary = (
    filtered_df
    .groupby("Category")
    .agg(
        Products=("Product ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique"),
        Average_Discount=("Discount", "mean")
    )
    .reset_index()
)

category_summary["Profit Margin %"] = (
    category_summary["Profit"]
    / category_summary["Sales"]
    * 100
)

category_summary["Average Discount %"] = (
    category_summary["Average_Discount"]
    * 100
)


# ============================================================
# CATEGORY SALES
# ============================================================

col1, col2 = st.columns(2)

with col1:

    fig_category_sales = px.bar(
        category_summary.sort_values(
            "Sales",
            ascending=False
        ),
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_category_sales,
        width="stretch"
    )


# ============================================================
# CATEGORY PROFIT
# ============================================================

with col2:

    fig_category_profit = px.bar(
        category_summary.sort_values(
            "Profit",
            ascending=False
        ),
        x="Category",
        y="Profit",
        title="Profit by Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_category_profit,
        width="stretch"
    )


# ============================================================
# SUB-CATEGORY SUMMARY
# ============================================================

st.markdown("---")

st.subheader("🏷️ Sub-Category Performance")

subcategory_summary = (
    filtered_df
    .groupby("Sub-Category")
    .agg(
        Products=("Product ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique"),
        Average_Discount=("Discount", "mean")
    )
    .reset_index()
)

subcategory_summary["Profit Margin %"] = (
    subcategory_summary["Profit"]
    / subcategory_summary["Sales"]
    * 100
)

subcategory_summary["Average Discount %"] = (
    subcategory_summary["Average_Discount"]
    * 100
)


# ============================================================
# SUB-CATEGORY SALES
# ============================================================

col1, col2 = st.columns(2)

with col1:

    fig_subcategory_sales = px.bar(
        subcategory_summary.sort_values(
            "Sales",
            ascending=True
        ),
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Sales by Sub-Category"
    )

    st.plotly_chart(
        fig_subcategory_sales,
        width="stretch"
    )


# ============================================================
# SUB-CATEGORY PROFIT
# ============================================================

with col2:

    fig_subcategory_profit = px.bar(
        subcategory_summary.sort_values(
            "Profit",
            ascending=True
        ),
        x="Profit",
        y="Sub-Category",
        orientation="h",
        title="Profit by Sub-Category"
    )

    st.plotly_chart(
        fig_subcategory_profit,
        width="stretch"
    )


# ============================================================
# PRODUCT SALES VS PROFIT
# ============================================================

st.markdown("---")

st.subheader("⚖️ Product Sales vs Profit")

fig_product_sales_profit = px.scatter(
    product_summary,
    x="Sales",
    y="Profit",
    size="Quantity",
    color="Category",
    hover_data=[
        "Product ID",
        "Product Name",
        "Sub-Category"
    ],
    title="Product Sales vs Profit"
)

st.plotly_chart(
    fig_product_sales_profit,
    width="stretch"
)


# ============================================================
# PRODUCT DISCOUNT VS PROFIT
# ============================================================

st.markdown("---")

st.subheader("🏷️ Product Discount vs Profit")

fig_product_discount_profit = px.scatter(
    product_summary,
    x="Average Discount %",
    y="Profit",
    size="Sales",
    color="Category",
    hover_data=[
        "Product ID",
        "Product Name",
        "Sub-Category"
    ],
    title="Product Discount vs Profit"
)

st.plotly_chart(
    fig_product_discount_profit,
    width="stretch"
)


# ============================================================
# CATEGORY / SUB-CATEGORY HIERARCHY
# ============================================================

st.markdown("---")

st.subheader("📂 Category → Sub-Category Performance")

hierarchy = (
    filtered_df
    .groupby(
        ["Category", "Sub-Category"],
        as_index=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Products=("Product ID", "nunique")
    )
)

fig_hierarchy = px.treemap(
    hierarchy,
    path=[
        "Category",
        "Sub-Category"
    ],
    values="Sales",
    color="Profit",
    hover_data=[
        "Quantity",
        "Products"
    ],
    title="Sales Hierarchy: Category → Sub-Category"
)

st.plotly_chart(
    fig_hierarchy,
    width="stretch"
)


# ============================================================
# CATEGORY PROFITABILITY
# ============================================================

st.markdown("---")

st.subheader("📊 Category Profit Margin")

category_margin = category_summary.sort_values(
    "Profit Margin %",
    ascending=False
)

fig_category_margin = px.bar(
    category_margin,
    x="Category",
    y="Profit Margin %",
    title="Profit Margin by Category",
    text_auto=".2f"
)

fig_category_margin.update_layout(
    yaxis_title="Profit Margin (%)"
)

st.plotly_chart(
    fig_category_margin,
    width="stretch"
)


# ============================================================
# PRODUCT SELECTOR
# ============================================================

st.markdown("---")

st.subheader("🔎 Product Detail")

product_options = (
    product_summary[
        [
            "Product ID",
            "Product Name"
        ]
    ]
    .drop_duplicates()
    .sort_values("Product Name")
)

selected_product = st.selectbox(
    "Select a Product",
    product_options["Product Name"].tolist()
)

selected_product_data = product_summary[
    product_summary["Product Name"] == selected_product
]

if not selected_product_data.empty:

    product_row = selected_product_data.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Sales",
            f"${product_row['Sales']:,.2f}"
        )

    with col2:
        st.metric(
            "Profit",
            f"${product_row['Profit']:,.2f}"
        )

    with col3:
        st.metric(
            "Quantity",
            f"{product_row['Quantity']:,}"
        )

    with col4:
        st.metric(
            "Profit Margin",
            f"{product_row['Profit Margin %']:.2f}%"
        )

    st.caption(
        f"Category: {product_row['Category']} | "
        f"Sub-Category: {product_row['Sub-Category']} | "
        f"Orders: {product_row['Orders']:,} | "
        f"Average Discount: "
        f"{product_row['Average Discount %']:.2f}%"
    )


# ============================================================
# PRODUCT PERFORMANCE TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Product Performance Table")

product_table = product_summary.copy()

product_table["Sales"] = (
    product_table["Sales"].round(2)
)

product_table["Profit"] = (
    product_table["Profit"].round(2)
)

product_table["Profit Margin %"] = (
    product_table["Profit Margin %"].round(2)
)

product_table["Average Discount %"] = (
    product_table["Average Discount %"].round(2)
)

product_table = product_table.sort_values(
    "Sales",
    ascending=False
)

st.markdown(
    product_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Product Data")

csv_data = product_table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Product Analysis",
    data=csv_data,
    file_name="product_analysis.csv",
    mime="text/csv"
)