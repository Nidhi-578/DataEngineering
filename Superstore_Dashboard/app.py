import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters
from utils.kpis import calculate_kpis

from utils.charts import (
    sales_by_region,
    sales_by_category,
    profit_by_category,
    monthly_sales_profit,
    top_subcategories,
    top_products
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = "data/sample_-_superstore.csv"

df = load_data(DATA_FILE)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = apply_filters(df)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Superstore Sales Analytics Dashboard")

st.markdown("### Executive Overview")


# ============================================================
# KPI CALCULATIONS
# ============================================================

kpis = calculate_kpis(filtered_df)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        label="Total Sales",
        value=f"${kpis['total_sales']:,.2f}"
    )


with col2:
    st.metric(
        label="Total Profit",
        value=f"${kpis['total_profit']:,.2f}"
    )


with col3:
    st.metric(
        label="Total Orders",
        value=f"{kpis['total_orders']:,}"
    )


with col4:
    st.metric(
        label="Total Quantity",
        value=f"{kpis['total_quantity']:,}"
    )


with col5:
    st.metric(
        label="Profit Margin",
        value=f"{kpis['profit_margin']:.2f}%"
    )


# ============================================================
# SALES & PROFIT BY REGION / CATEGORY
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.plotly_chart(
        sales_by_region(filtered_df),
        width="stretch"
    )


with col2:

    st.plotly_chart(
        sales_by_category(filtered_df),
        width="stretch"
    )


# ============================================================
# PROFIT BY CATEGORY
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.plotly_chart(
        profit_by_category(filtered_df),
        width="stretch"
    )


# ============================================================
# MONTHLY SALES & PROFIT TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Monthly Sales & Profit Trend")

st.plotly_chart(
    monthly_sales_profit(filtered_df),
    width="stretch"
)


# ============================================================
# TOP 10 SUB-CATEGORIES & PRODUCTS
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.plotly_chart(
        top_subcategories(filtered_df),
        width="stretch"
    )


with col2:

    st.plotly_chart(
        top_products(filtered_df),
        width="stretch"
    )


# ============================================================
# CSV DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_superstore_data.csv",
    mime="text/csv"
)
