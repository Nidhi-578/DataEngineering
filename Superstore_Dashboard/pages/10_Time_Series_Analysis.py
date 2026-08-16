import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Time Series Analysis",
    page_icon="📈",
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

st.title("📈 Time Series Analysis")

st.markdown(
    "Analyze sales, profit and order trends over time, "
    "including growth, seasonality and year-over-year performance."
)


# ============================================================
# PREPARE DATE COLUMNS
# ============================================================

filtered_df["Order Date"] = pd.to_datetime(
    filtered_df["Order Date"]
)

filtered_df["Year"] = (
    filtered_df["Order Date"].dt.year
)

filtered_df["Month"] = (
    filtered_df["Order Date"].dt.month
)

filtered_df["Month Name"] = (
    filtered_df["Order Date"].dt.strftime("%b")
)


# ============================================================
# MONTHLY SUMMARY
# ============================================================

monthly_summary = (
    filtered_df
    .set_index("Order Date")
    .resample("MS")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

monthly_summary["Profit Margin %"] = (
    monthly_summary["Profit"]
    / monthly_summary["Sales"]
    * 100
)


# ============================================================
# GROWTH CALCULATIONS
# ============================================================

monthly_summary["Sales Growth %"] = (
    monthly_summary["Sales"]
    .pct_change()
    * 100
)

monthly_summary["Profit Growth %"] = (
    monthly_summary["Profit"]
    .pct_change()
    * 100
)

monthly_summary["Order Growth %"] = (
    monthly_summary["Orders"]
    .pct_change()
    * 100
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = monthly_summary["Sales"].sum()

total_profit = monthly_summary["Profit"].sum()

total_orders = monthly_summary["Orders"].sum()

average_monthly_sales = (
    monthly_summary["Sales"].mean()
    if len(monthly_summary) > 0
    else 0
)

best_sales_month = (
    monthly_summary.loc[
        monthly_summary["Sales"].idxmax(),
        "Order Date"
    ].strftime("%b %Y")
    if len(monthly_summary) > 0
    else "N/A"
)

best_profit_month = (
    monthly_summary.loc[
        monthly_summary["Profit"].idxmax(),
        "Order Date"
    ].strftime("%b %Y")
    if len(monthly_summary) > 0
    else "N/A"
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Time Series KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col4:
    st.metric(
        "Avg Monthly Sales",
        f"${average_monthly_sales:,.0f}"
    )

with col5:
    st.metric(
        "Best Sales Month",
        best_sales_month
    )


# ============================================================
# MONTHLY SALES TREND
# ============================================================

st.markdown("---")

st.subheader("💰 Monthly Sales Trend")

fig_monthly_sales = px.line(
    monthly_summary,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)

fig_monthly_sales.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_monthly_sales,
    width="stretch"
)


# ============================================================
# MONTHLY PROFIT TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Monthly Profit Trend")

fig_monthly_profit = px.line(
    monthly_summary,
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
# SALES VS PROFIT TREND
# ============================================================

st.markdown("---")

st.subheader("⚖️ Sales vs Profit Over Time")

sales_profit = monthly_summary.melt(
    id_vars="Order Date",
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_sales_profit = px.line(
    sales_profit,
    x="Order Date",
    y="Amount",
    color="Metric",
    markers=True,
    title="Sales vs Profit Trend"
)

st.plotly_chart(
    fig_sales_profit,
    width="stretch"
)


# ============================================================
# MONTHLY ORDERS TREND
# ============================================================

st.markdown("---")

st.subheader("🧾 Monthly Order Trend")

fig_monthly_orders = px.bar(
    monthly_summary,
    x="Order Date",
    y="Orders",
    title="Monthly Orders",
    text_auto=True
)

fig_monthly_orders.update_layout(
    xaxis_title="Month",
    yaxis_title="Orders"
)

st.plotly_chart(
    fig_monthly_orders,
    width="stretch"
)


# ============================================================
# SALES GROWTH
# ============================================================

st.markdown("---")

st.subheader("📊 Monthly Sales Growth")

sales_growth_display = monthly_summary.dropna(
    subset=["Sales Growth %"]
)

fig_sales_growth = px.bar(
    sales_growth_display,
    x="Order Date",
    y="Sales Growth %",
    title="Month-over-Month Sales Growth",
    text_auto=".1f"
)

fig_sales_growth.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales Growth (%)"
)

st.plotly_chart(
    fig_sales_growth,
    width="stretch"
)


# ============================================================
# PROFIT GROWTH
# ============================================================

st.subheader("📈 Monthly Profit Growth")

profit_growth_display = monthly_summary.dropna(
    subset=["Profit Growth %"]
)

fig_profit_growth = px.bar(
    profit_growth_display,
    x="Order Date",
    y="Profit Growth %",
    title="Month-over-Month Profit Growth",
    text_auto=".1f"
)

fig_profit_growth.update_layout(
    xaxis_title="Month",
    yaxis_title="Profit Growth (%)"
)

st.plotly_chart(
    fig_profit_growth,
    width="stretch"
)


# ============================================================
# YEARLY SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📅 Yearly Performance")

yearly_summary = (
    filtered_df
    .groupby("Year")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

yearly_summary["Profit Margin %"] = (
    yearly_summary["Profit"]
    / yearly_summary["Sales"]
    * 100
)

yearly_summary["Sales Growth %"] = (
    yearly_summary["Sales"]
    .pct_change()
    * 100
)

yearly_summary["Profit Growth %"] = (
    yearly_summary["Profit"]
    .pct_change()
    * 100
)


# ============================================================
# YEARLY SALES CHART
# ============================================================

col1, col2 = st.columns(2)

with col1:

    fig_year_sales = px.bar(
        yearly_summary,
        x="Year",
        y="Sales",
        title="Sales by Year",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_year_sales,
        width="stretch"
    )


# ============================================================
# YEARLY PROFIT CHART
# ============================================================

with col2:

    fig_year_profit = px.bar(
        yearly_summary,
        x="Year",
        y="Profit",
        title="Profit by Year",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_year_profit,
        width="stretch"
    )


# ============================================================
# YEARLY SUMMARY TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Yearly Summary")

yearly_display = yearly_summary.copy()

yearly_display["Sales"] = (
    yearly_display["Sales"].round(2)
)

yearly_display["Profit"] = (
    yearly_display["Profit"].round(2)
)

yearly_display["Profit Margin %"] = (
    yearly_display["Profit Margin %"].round(2)
)

yearly_display["Sales Growth %"] = (
    yearly_display["Sales Growth %"].round(2)
)

yearly_display["Profit Growth %"] = (
    yearly_display["Profit Growth %"].round(2)
)

st.markdown(
    yearly_display.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# MONTHLY SEASONALITY
# ============================================================

st.markdown("---")

st.subheader("🗓️ Monthly Seasonality")

seasonality = (
    filtered_df
    .groupby("Month")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

month_names = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

seasonality["Month Name"] = (
    seasonality["Month"]
    .map(month_names)
)

fig_seasonality = px.line(
    seasonality,
    x="Month Name",
    y="Sales",
    markers=True,
    title="Sales Seasonality by Month"
)

st.plotly_chart(
    fig_seasonality,
    width="stretch"
)


# ============================================================
# SEASONAL PROFIT
# ============================================================

st.subheader("💰 Profit Seasonality")

fig_profit_seasonality = px.line(
    seasonality,
    x="Month Name",
    y="Profit",
    markers=True,
    title="Profit Seasonality by Month"
)

st.plotly_chart(
    fig_profit_seasonality,
    width="stretch"
)


# ============================================================
# CATEGORY TREND
# ============================================================

st.markdown("---")

st.subheader("📦 Sales Trend by Category")

category_monthly = (
    filtered_df
    .set_index("Order Date")
    .groupby("Category")
    .resample("MS")["Sales"]
    .sum()
    .reset_index()
)

fig_category_trend = px.line(
    category_monthly,
    x="Order Date",
    y="Sales",
    color="Category",
    markers=True,
    title="Monthly Sales by Category"
)

st.plotly_chart(
    fig_category_trend,
    width="stretch"
)


# ============================================================
# REGION TREND
# ============================================================

st.markdown("---")

st.subheader("🌎 Sales Trend by Region")

region_monthly = (
    filtered_df
    .set_index("Order Date")
    .groupby("Region")
    .resample("MS")["Sales"]
    .sum()
    .reset_index()
)

fig_region_trend = px.line(
    region_monthly,
    x="Order Date",
    y="Sales",
    color="Region",
    markers=True,
    title="Monthly Sales by Region"
)

st.plotly_chart(
    fig_region_trend,
    width="stretch"
)


# ============================================================
# BEST AND WORST MONTHS
# ============================================================

st.markdown("---")

st.subheader("🏆 Best and Worst Performing Months")

best_months = (
    monthly_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(5)
    .copy()
)

worst_months = (
    monthly_summary
    .sort_values(
        "Sales",
        ascending=True
    )
    .head(5)
    .copy()
)

best_months["Month"] = (
    best_months["Order Date"]
    .dt.strftime("%b %Y")
)

worst_months["Month"] = (
    worst_months["Order Date"]
    .dt.strftime("%b %Y")
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🟢 Top 5 Sales Months")

    best_display = best_months[
        [
            "Month",
            "Sales",
            "Profit",
            "Orders"
        ]
    ].copy()

    best_display["Sales"] = (
        best_display["Sales"].round(2)
    )

    best_display["Profit"] = (
        best_display["Profit"].round(2)
    )

    st.markdown(
        best_display.to_html(
            index=False,
            border=0
        ),
        unsafe_allow_html=True
    )


with col2:

    st.markdown("### 🔴 Bottom 5 Sales Months")

    worst_display = worst_months[
        [
            "Month",
            "Sales",
            "Profit",
            "Orders"
        ]
    ].copy()

    worst_display["Sales"] = (
        worst_display["Sales"].round(2)
    )

    worst_display["Profit"] = (
        worst_display["Profit"].round(2)
    )

    st.markdown(
        worst_display.to_html(
            index=False,
            border=0
        ),
        unsafe_allow_html=True
    )


# ============================================================
# MONTHLY SUMMARY TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Monthly Summary")

monthly_display = monthly_summary.copy()

monthly_display["Month"] = (
    monthly_display["Order Date"]
    .dt.strftime("%Y-%m")
)

monthly_display["Sales"] = (
    monthly_display["Sales"].round(2)
)

monthly_display["Profit"] = (
    monthly_display["Profit"].round(2)
)

monthly_display["Profit Margin %"] = (
    monthly_display["Profit Margin %"].round(2)
)

monthly_display["Sales Growth %"] = (
    monthly_display["Sales Growth %"].round(2)
)

monthly_display["Profit Growth %"] = (
    monthly_display["Profit Growth %"].round(2)
)

monthly_display["Order Growth %"] = (
    monthly_display["Order Growth %"].round(2)
)

monthly_display = monthly_display[
    [
        "Month",
        "Sales",
        "Profit",
        "Orders",
        "Quantity",
        "Profit Margin %",
        "Sales Growth %",
        "Profit Growth %",
        "Order Growth %"
    ]
]

# HTML table instead of st.dataframe()
# because PyArrow is blocked on this machine.

st.markdown(
    monthly_display.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Time Series Data")

csv_data = monthly_display.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Time Series Analysis",
    data=csv_data,
    file_name="time_series_analysis.csv",
    mime="text/csv"
)