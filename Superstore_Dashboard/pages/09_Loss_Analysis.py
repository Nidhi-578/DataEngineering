import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.filters import apply_filters


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loss Analysis",
    page_icon="🔻",
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

st.title("🔻 Loss Analysis")

st.markdown(
    "Identify loss-making orders, products, customers, "
    "categories and regions, and understand the impact of discounts."
)


# ============================================================
# LOSS-MAKING RECORDS
# ============================================================

loss_df = filtered_df[
    filtered_df["Profit"] < 0
].copy()


# ============================================================
# BASIC LOSS METRICS
# ============================================================

total_loss = loss_df["Profit"].sum()

loss_amount = abs(total_loss)

loss_records = len(loss_df)

loss_orders = loss_df["Order ID"].nunique()

loss_customers = loss_df["Customer ID"].nunique()

loss_products = loss_df["Product ID"].nunique()

loss_percentage = (
    loss_records / len(filtered_df) * 100
    if len(filtered_df) > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Loss KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Loss",
        f"${loss_amount:,.2f}"
    )

with col2:
    st.metric(
        "Loss-Making Orders",
        f"{loss_orders:,}"
    )

with col3:
    st.metric(
        "Loss-Making Customers",
        f"{loss_customers:,}"
    )

with col4:
    st.metric(
        "Loss-Making Products",
        f"{loss_products:,}"
    )

with col5:
    st.metric(
        "% Loss Records",
        f"{loss_percentage:.2f}%"
    )


# ============================================================
# LOSS BY CATEGORY
# ============================================================

st.markdown("---")

st.subheader("📦 Loss by Category")

category_loss = (
    loss_df
    .groupby(
        "Category",
        as_index=False
    )["Profit"]
    .sum()
    .sort_values(
        "Profit",
        ascending=True
    )
)

category_loss["Loss"] = (
    category_loss["Profit"].abs()
)

fig_category_loss = px.bar(
    category_loss,
    x="Profit",
    y="Category",
    orientation="h",
    title="Loss by Category"
)

st.plotly_chart(
    fig_category_loss,
    width="stretch"
)


# ============================================================
# LOSS BY SUB-CATEGORY
# ============================================================

st.subheader("🏷️ Loss by Sub-Category")

subcategory_loss = (
    loss_df
    .groupby(
        "Sub-Category",
        as_index=False
    )["Profit"]
    .sum()
    .sort_values(
        "Profit",
        ascending=True
    )
)

fig_subcategory_loss = px.bar(
    subcategory_loss,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    title="Loss by Sub-Category"
)

st.plotly_chart(
    fig_subcategory_loss,
    width="stretch"
)


# ============================================================
# LOSS BY REGION
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌎 Loss by Region")

    region_loss = (
        loss_df
        .groupby(
            "Region",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=True
        )
    )

    fig_region_loss = px.bar(
        region_loss,
        x="Region",
        y="Profit",
        title="Loss by Region",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_region_loss,
        width="stretch"
    )


# ============================================================
# LOSS BY SEGMENT
# ============================================================

with col2:

    st.subheader("👥 Loss by Segment")

    segment_loss = (
        loss_df
        .groupby(
            "Segment",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=True
        )
    )

    fig_segment_loss = px.bar(
        segment_loss,
        x="Segment",
        y="Profit",
        title="Loss by Segment",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_segment_loss,
        width="stretch"
    )


# ============================================================
# LOSS BY STATE
# ============================================================

st.markdown("---")

st.subheader("📍 Top Loss-Making States")

state_loss = (
    loss_df
    .groupby(
        "State/Province",
        as_index=False
    )["Profit"]
    .sum()
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(15)
)

fig_state_loss = px.bar(
    state_loss,
    x="Profit",
    y="State/Province",
    orientation="h",
    title="Top 15 Loss-Making States"
)

st.plotly_chart(
    fig_state_loss,
    width="stretch"
)


# ============================================================
# LOSS BY CITY
# ============================================================

st.subheader("🏙️ Top Loss-Making Cities")

city_loss = (
    loss_df
    .groupby(
        "City",
        as_index=False
    )["Profit"]
    .sum()
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(15)
)

fig_city_loss = px.bar(
    city_loss,
    x="Profit",
    y="City",
    orientation="h",
    title="Top 15 Loss-Making Cities"
)

st.plotly_chart(
    fig_city_loss,
    width="stretch"
)


# ============================================================
# TOP LOSS-MAKING PRODUCTS
# ============================================================

st.markdown("---")

st.subheader("🔻 Top Loss-Making Products")

product_loss = (
    loss_df
    .groupby(
        ["Product ID", "Product Name"],
        as_index=False
    )
    .agg(
        Profit=("Profit", "sum"),
        Sales=("Sales", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(15)
)

fig_product_loss = px.bar(
    product_loss.sort_values("Profit"),
    x="Profit",
    y="Product Name",
    orientation="h",
    title="Top 15 Loss-Making Products"
)

st.plotly_chart(
    fig_product_loss,
    width="stretch"
)


# ============================================================
# TOP LOSS-MAKING CUSTOMERS
# ============================================================

st.subheader("👤 Top Loss-Making Customers")

customer_loss = (
    loss_df
    .groupby(
        "Customer Name",
        as_index=False
    )
    .agg(
        Profit=("Profit", "sum"),
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique")
    )
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(15)
)

fig_customer_loss = px.bar(
    customer_loss.sort_values("Profit"),
    x="Profit",
    y="Customer Name",
    orientation="h",
    title="Top 15 Loss-Making Customers"
)

st.plotly_chart(
    fig_customer_loss,
    width="stretch"
)


# ============================================================
# DISCOUNT VS LOSS
# ============================================================

st.markdown("---")

st.subheader("🏷️ Discount vs Loss")

fig_discount_loss = px.scatter(
    loss_df,
    x="Discount",
    y="Profit",
    size="Sales",
    color="Category",
    hover_data=[
        "Order ID",
        "Product Name",
        "Customer Name",
        "Region"
    ],
    title="Discount vs Loss-Making Profit"
)

fig_discount_loss.update_layout(
    xaxis_title="Discount",
    yaxis_title="Profit"
)

st.plotly_chart(
    fig_discount_loss,
    width="stretch"
)


# ============================================================
# LOSS BY DISCOUNT BAND
# ============================================================

st.subheader("📊 Loss by Discount Band")

loss_band = loss_df.copy()

loss_band["Discount Band"] = pd.cut(
    loss_band["Discount"],
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

loss_by_band = (
    loss_band
    .groupby(
        "Discount Band",
        observed=False
    )
    .agg(
        Loss=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

loss_by_band["Loss Amount"] = (
    loss_by_band["Loss"].abs()
)

fig_loss_band = px.bar(
    loss_by_band,
    x="Discount Band",
    y="Loss Amount",
    title="Loss Amount by Discount Band",
    text_auto=".2s"
)

st.plotly_chart(
    fig_loss_band,
    width="stretch"
)


# ============================================================
# LOSS-MAKING ORDERS
# ============================================================

st.markdown("---")

st.subheader("🧾 Top Loss-Making Orders")

order_loss = (
    loss_df
    .groupby(
        "Order ID",
        as_index=False
    )
    .agg(
        Customer=("Customer Name", "first"),
        Region=("Region", "first"),
        Category=("Category", "first"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Average_Discount=("Discount", "mean")
    )
    .sort_values(
        "Profit",
        ascending=True
    )
    .head(25)
)

order_loss["Average Discount %"] = (
    order_loss["Average_Discount"] * 100
)

order_loss["Sales"] = (
    order_loss["Sales"].round(2)
)

order_loss["Profit"] = (
    order_loss["Profit"].round(2)
)

order_loss["Average Discount %"] = (
    order_loss["Average Discount %"].round(2)
)

st.markdown(
    order_loss[
        [
            "Order ID",
            "Customer",
            "Region",
            "Category",
            "Sales",
            "Profit",
            "Quantity",
            "Average Discount %"
        ]
    ].to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# LOSS BY SHIP MODE
# ============================================================

st.markdown("---")

st.subheader("🚚 Loss by Ship Mode")

ship_mode_loss = (
    loss_df
    .groupby(
        "Ship Mode",
        as_index=False
    )["Profit"]
    .sum()
    .sort_values(
        "Profit",
        ascending=True
    )
)

fig_ship_mode_loss = px.bar(
    ship_mode_loss,
    x="Ship Mode",
    y="Profit",
    title="Loss by Ship Mode",
    text_auto=".2s"
)

st.plotly_chart(
    fig_ship_mode_loss,
    width="stretch"
)


# ============================================================
# LOSS SUMMARY TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Loss Summary")

loss_summary = pd.DataFrame({
    "Metric": [
        "Total Loss",
        "Loss-Making Records",
        "Loss-Making Orders",
        "Loss-Making Customers",
        "Loss-Making Products",
        "Loss Record Percentage"
    ],
    "Value": [
        f"${loss_amount:,.2f}",
        f"{loss_records:,}",
        f"{loss_orders:,}",
        f"{loss_customers:,}",
        f"{loss_products:,}",
        f"{loss_percentage:.2f}%"
    ]
})

st.markdown(
    loss_summary.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DETAILED LOSS TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Detailed Loss-Making Records")

loss_table = loss_df[
    [
        "Order ID",
        "Order Date",
        "Customer Name",
        "Region",
        "State/Province",
        "City",
        "Category",
        "Sub-Category",
        "Product Name",
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    ]
].copy()

loss_table = loss_table.sort_values(
    "Profit",
    ascending=True
)

loss_table["Order Date"] = (
    pd.to_datetime(
        loss_table["Order Date"]
    ).dt.strftime("%Y-%m-%d")
)

loss_table["Sales"] = (
    loss_table["Sales"].round(2)
)

loss_table["Discount %"] = (
    loss_table["Discount"] * 100
)

loss_table["Profit"] = (
    loss_table["Profit"].round(2)
)

loss_table["Discount %"] = (
    loss_table["Discount %"].round(2)
)

st.markdown(
    loss_table.to_html(
        index=False,
        border=0
    ),
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader("📥 Download Loss Data")

csv_data = loss_table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Loss Analysis",
    data=csv_data,
    file_name="loss_analysis.csv",
    mime="text/csv"
)