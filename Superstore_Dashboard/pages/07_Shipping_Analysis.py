import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Shipping Analysis",
    page_icon="🚚",
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

st.title("🚚 Shipping Analysis")

st.markdown(
    "Analyze shipping performance, delivery time, shipping modes, "
    "sales and profitability."
)


# ============================================================
# ENSURE DATE COLUMNS ARE DATETIME
# ============================================================

filtered_df["Order Date"] = pd.to_datetime(
    filtered_df["Order Date"]
)

filtered_df["Ship Date"] = pd.to_datetime(
    filtered_df["Ship Date"]
)


# ============================================================
# CALCULATE SHIPPING DAYS
# ============================================================

filtered_df["Shipping Days"] = (
    filtered_df["Ship Date"]
    - filtered_df["Order Date"]
).dt.days


# ============================================================
# ORDER-LEVEL SHIPPING SUMMARY
# ============================================================

shipping_summary = (
    filtered_df
    .groupby("Order ID")
    .agg(
        Order_Date=("Order Date", "min"),
        Ship_Date=("Ship Date", "max"),
        Ship_Mode=("Ship Mode", "first"),
        Customer=("Customer Name", "first"),
        Region=("Region", "first"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Shipping_Days=("Shipping Days", "max")
    )
    .reset_index()
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = shipping_summary["Order ID"].nunique()

average_shipping_days = (
    shipping_summary["Shipping_Days"].mean()
    if total_orders > 0
    else 0
)

fastest_shipping = (
    shipping_summary["Shipping_Days"].min()
    if total_orders > 0
    else 0
)

slowest_shipping = (
    shipping_summary["Shipping_Days"].max()
    if total_orders > 0
    else 0
)

total_sales = shipping_summary["Sales"].sum()

total_profit = shipping_summary["Profit"].sum()


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Shipping KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col2:
    st.metric(
        "Avg Shipping Days",
        f"{average_shipping_days:.2f}"
    )

with col3:
    st.metric(
        "Fastest Shipping",
        f"{fastest_shipping:.0f} days"
    )

with col4:
    st.metric(
        "Slowest Shipping",
        f"{slowest_shipping:.0f} days"
    )

with col5:
    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )


# ============================================================
# SHIPPING DAYS DISTRIBUTION
# ============================================================

st.markdown("---")

st.subheader("⏱️ Shipping Days Distribution")

fig_shipping_distribution = px.histogram(
    shipping_summary,
    x="Shipping_Days",
    nbins=20,
    title="Distribution of Shipping Days"
)

fig_shipping_distribution.update_layout(
    xaxis_title="Shipping Days",
    yaxis_title="Number of Orders"
)

st.plotly_chart(
    fig_shipping_distribution,
    width="stretch"
)


# ============================================================
# SHIPPING DAYS SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📊 Shipping Time Summary")

shipping_days_summary = (
    shipping_summary["Shipping_Days"]
    .describe()
    .reset_index()
)

shipping_days_summary.columns = [
    "Metric",
    "Shipping Days"
]

shipping_days_summary["Shipping Days"] = (
    shipping_days_summary["Shipping Days"]
    .round(2)
)

st.markdown(
    shipping_days_summary.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# SHIP MODE PERFORMANCE
# ============================================================

st.markdown("---")

st.subheader("🚛 Ship Mode Performance")

ship_mode_summary = (
    shipping_summary
    .groupby("Ship_Mode")
    .agg(
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Average_Shipping_Days=("Shipping_Days", "mean")
    )
    .reset_index()
)

ship_mode_summary["Profit Margin %"] = (
    ship_mode_summary["Profit"]
    / ship_mode_summary["Sales"]
    * 100
)

ship_mode_summary["Average Shipping Days"] = (
    ship_mode_summary["Average_Shipping_Days"]
    .round(2)
)

ship_mode_summary["Profit Margin %"] = (
    ship_mode_summary["Profit Margin %"]
    .round(2)
)


# ============================================================
# SHIP MODE CHARTS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    fig_ship_mode_orders = px.bar(
        ship_mode_summary.sort_values(
            "Orders",
            ascending=False
        ),
        x="Ship_Mode",
        y="Orders",
        title="Orders by Ship Mode",
        text_auto=True
    )

    st.plotly_chart(
        fig_ship_mode_orders,
        width="stretch"
    )


with col2:

    fig_ship_mode_days = px.bar(
        ship_mode_summary.sort_values(
            "Average_Shipping_Days",
            ascending=True
        ),
        x="Ship_Mode",
        y="Average_Shipping_Days",
        title="Average Shipping Days by Ship Mode",
        text_auto=".2f"
    )

    fig_ship_mode_days.update_layout(
        yaxis_title="Average Shipping Days"
    )

    st.plotly_chart(
        fig_ship_mode_days,
        width="stretch"
    )


# ============================================================
# SALES AND PROFIT BY SHIP MODE
# ============================================================

col1, col2 = st.columns(2)

with col1:

    fig_ship_sales = px.bar(
        ship_mode_summary.sort_values(
            "Sales",
            ascending=False
        ),
        x="Ship_Mode",
        y="Sales",
        title="Sales by Ship Mode",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_ship_sales,
        width="stretch"
    )


with col2:

    fig_ship_profit = px.bar(
        ship_mode_summary.sort_values(
            "Profit",
            ascending=False
        ),
        x="Ship_Mode",
        y="Profit",
        title="Profit by Ship Mode",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_ship_profit,
        width="stretch"
    )


# ============================================================
# SHIP MODE SUMMARY TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Ship Mode Summary")

ship_mode_display = ship_mode_summary[
    [
        "Ship_Mode",
        "Orders",
        "Sales",
        "Profit",
        "Average Shipping Days",
        "Profit Margin %"
    ]
].copy()

ship_mode_display["Sales"] = (
    ship_mode_display["Sales"]
    .round(2)
)

ship_mode_display["Profit"] = (
    ship_mode_display["Profit"]
    .round(2)
)

st.markdown(
    ship_mode_display.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# SHIPPING TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Average Shipping Days Over Time")

monthly_shipping = (
    shipping_summary
    .set_index("Order_Date")
    .resample("MS")["Shipping_Days"]
    .mean()
    .reset_index()
)

fig_shipping_trend = px.line(
    monthly_shipping,
    x="Order_Date",
    y="Shipping_Days",
    markers=True,
    title="Monthly Average Shipping Days"
)

fig_shipping_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Shipping Days"
)

st.plotly_chart(
    fig_shipping_trend,
    width="stretch"
)


# ============================================================
# SHIPPING BY REGION
# ============================================================

st.markdown("---")

st.subheader("🌎 Shipping Performance by Region")

region_shipping = (
    shipping_summary
    .groupby("Region")
    .agg(
        Orders=("Order ID", "nunique"),
        Average_Shipping_Days=("Shipping_Days", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

region_shipping["Average Shipping Days"] = (
    region_shipping["Average_Shipping_Days"]
    .round(2)
)

col1, col2 = st.columns(2)

with col1:

    fig_region_days = px.bar(
        region_shipping.sort_values(
            "Average_Shipping_Days",
            ascending=True
        ),
        x="Region",
        y="Average_Shipping_Days",
        title="Average Shipping Days by Region",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_region_days,
        width="stretch"
    )


with col2:

    fig_region_orders = px.bar(
        region_shipping.sort_values(
            "Orders",
            ascending=False
        ),
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
# SHIPPING BY CATEGORY
# ============================================================

st.markdown("---")

st.subheader("📦 Shipping Performance by Category")

category_shipping = (
    filtered_df
    .groupby("Category")
    .agg(
        Orders=("Order ID", "nunique"),
        Average_Shipping_Days=("Shipping Days", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_shipping["Average Shipping Days"] = (
    category_shipping["Average_Shipping_Days"]
    .round(2)
)

fig_category_shipping = px.bar(
    category_shipping,
    x="Category",
    y="Average_Shipping_Days",
    title="Average Shipping Days by Category",
    text_auto=".2f"
)

st.plotly_chart(
    fig_category_shipping,
    width="stretch"
)


# ============================================================
# SHIPPING DAYS VS SALES
# ============================================================

st.markdown("---")

st.subheader("⏱️ Shipping Days vs Sales")

fig_shipping_sales = px.scatter(
    shipping_summary,
    x="Shipping_Days",
    y="Sales",
    size="Quantity",
    color="Ship_Mode",
    hover_data=[
        "Order ID",
        "Region",
        "Customer"
    ],
    title="Shipping Days vs Order Sales"
)

fig_shipping_sales.update_layout(
    xaxis_title="Shipping Days",
    yaxis_title="Order Sales"
)

st.plotly_chart(
    fig_shipping_sales,
    width="stretch"
)


# ============================================================
# DETAILED SHIPPING TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Shipping Data")

shipping_table = shipping_summary[
    [
        "Order ID",
        "Order_Date",
        "Ship_Date",
        "Ship_Mode",
        "Customer",
        "Region",
        "Sales",
        "Profit",
        "Quantity",
        "Shipping_Days"
    ]
].copy()

shipping_table = shipping_table.sort_values(
    "Shipping_Days",
    ascending=False
)

shipping_table["Order_Date"] = (
    shipping_table["Order_Date"]
    .dt.strftime("%Y-%m-%d")
)

shipping_table["Ship_Date"] = (
    shipping_table["Ship_Date"]
    .dt.strftime("%Y-%m-%d")
)

shipping_table["Sales"] = (
    shipping_table["Sales"]
    .round(2)
)

shipping_table["Profit"] = (
    shipping_table["Profit"]
    .round(2)
)

# HTML table instead of st.dataframe()
# because PyArrow is blocked on this machine.

st.markdown(
    shipping_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Shipping Data")

csv_data = shipping_table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Shipping Analysis",
    data=csv_data,
    file_name="shipping_analysis.csv",
    mime="text/csv"
)