import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    risk_segment_summary,
    risk_segment_income_summary,
    risk_segment_contract_summary,
    high_risk_customer_summary,
)


st.set_page_config(
    page_title="Combined Risk Segmentation",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading combined risk segmentation..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🎯 Combined Risk Segmentation")

st.markdown(
    """
    A combined risk view using external credit scores,
    credit burden, annuity burden, and regional risk.
    """
)


# ============================================================
# ANALYSIS
# ============================================================

risk_data = risk_segment_summary(df)

income_risk = risk_segment_income_summary(df)

contract_risk = risk_segment_contract_summary(df)

high_risk = high_risk_customer_summary(df)


# ============================================================
# KPI CARDS
# ============================================================

total_customers = len(df)

high_risk_customers = high_risk["customers"]

high_risk_percentage = (
    high_risk_customers /
    total_customers *
    100
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "High + Very High Risk",
        f"{high_risk_customers:,}"
    )

with col3:
    st.metric(
        "High-Risk Population",
        f"{high_risk_percentage:.1f}%"
    )

with col4:
    st.metric(
        "High-Risk Default Rate",
        f"{high_risk['default_rate']:.2f}%"
    )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Customer Distribution by Risk Category")

risk_display = risk_data.copy()

risk_display["default_rate"] = (
    risk_display["default_rate"].round(2)
)

st.dataframe(
    risk_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DEFAULT RATE BY RISK
# ============================================================

fig_risk = px.bar(
    risk_data,
    x="RISK_CATEGORY",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Observed Default Rate by Combined Risk Category"
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_risk.update_xaxes(
    title="Risk Category"
)

fig_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# CUSTOMER DISTRIBUTION
# ============================================================

fig_distribution = px.pie(
    risk_data,
    names="RISK_CATEGORY",
    values="customers",
    hole=0.45,
    title="Customer Distribution by Risk Category"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# RISK × INCOME
# ============================================================

st.divider()

st.subheader("💰 Risk Category × Income Group")

income_display = income_risk.copy()

income_display["default_rate"] = (
    income_display["default_rate"].round(2)
)

fig_income = px.density_heatmap(
    income_risk,
    x="INCOME_GROUP",
    y="RISK_CATEGORY",
    z="default_rate",
    text_auto=".2f",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Risk Category and Income Group"
)

fig_income.update_xaxes(
    title="Income Group"
)

fig_income.update_yaxes(
    title="Risk Category"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)

st.dataframe(
    income_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# RISK × CONTRACT
# ============================================================

st.divider()

st.subheader("📄 Risk Category × Contract Type")

contract_display = contract_risk.copy()

contract_display["default_rate"] = (
    contract_display["default_rate"].round(2)
)

fig_contract = px.bar(
    contract_risk,
    x="RISK_CATEGORY",
    y="default_rate",
    color="NAME_CONTRACT_TYPE",
    barmode="group",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Risk Category and Contract Type"
)

fig_contract.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_contract.update_xaxes(
    title="Risk Category"
)

fig_contract.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_contract,
    use_container_width=True
)

st.dataframe(
    contract_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HIGH-RISK CUSTOMER PROFILE
# ============================================================

st.divider()

st.subheader("🔴 High-Risk Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Income",
        f"{high_risk['average_income']:,.0f}"
    )

with col2:
    st.metric(
        "Average Credit",
        f"{high_risk['average_credit']:,.0f}"
    )

with col3:
    st.metric(
        "Average External Score",
        f"{high_risk['average_external_score']:.3f}"
    )


# ============================================================
# RISK GAP
# ============================================================

st.subheader("📈 Risk Gap")

low_risk = risk_data[
    risk_data["RISK_CATEGORY"] == "Low Risk"
]

very_high_risk = risk_data[
    risk_data["RISK_CATEGORY"] == "Very High Risk"
]

if not low_risk.empty and not very_high_risk.empty:

    low_rate = low_risk.iloc[0]["default_rate"]

    very_high_rate = (
        very_high_risk.iloc[0]["default_rate"]
    )

    risk_gap = very_high_rate - low_rate

    st.info(
        f"""
        The observed default rate increases from
        **{low_rate:.2f}%** in the Low Risk category to
        **{very_high_rate:.2f}%** in the Very High Risk category.

        Difference:
        **{risk_gap:.2f} percentage points**
        """
    )


# ============================================================
# RISK TABLE
# ============================================================

st.divider()

st.subheader("📋 Complete Risk Segmentation Summary")

st.dataframe(
    risk_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Business Insights")

highest_risk = risk_data.loc[
    risk_data["default_rate"].idxmax()
]

lowest_risk = risk_data.loc[
    risk_data["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:

    st.warning(
        f"""
        **Highest Observed Risk**

        Category:
        **{highest_risk['RISK_CATEGORY']}**

        Default Rate:
        **{highest_risk['default_rate']:.2f}%**

        Customers:
        **{highest_risk['customers']:,}**
        """
    )

with col2:

    st.success(
        f"""
        **Lowest Observed Risk**

        Category:
        **{lowest_risk['RISK_CATEGORY']}**

        Default Rate:
        **{lowest_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_risk['customers']:,}**
        """
    )


st.caption(
    "Combined risk categories are analytical segments created "
    "from multiple observed customer attributes. Default rates "
    "describe historical patterns and should not be interpreted "
    "as causal or as individual credit decisions."
)