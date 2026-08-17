import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    portfolio_summary,
    portfolio_risk_distribution,
    portfolio_contract_summary,
    portfolio_credit_exposure,
    portfolio_income_credit_summary,
    portfolio_risk_metrics,
)


st.set_page_config(
    page_title="Portfolio Risk Summary",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading portfolio summary..."):
    df = load_data()


# ============================================================
# ANALYSIS
# ============================================================

summary = portfolio_summary(df)

risk_distribution = portfolio_risk_distribution(df)

contract_summary = portfolio_contract_summary(df)

credit_exposure = portfolio_credit_exposure(df)

income_credit = portfolio_income_credit_summary(df)

risk_metrics = portfolio_risk_metrics(df)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Portfolio Risk & Business Summary")

st.markdown(
    """
    Executive-level view of portfolio size, credit exposure,
    customer risk distribution, contract mix and financial profile.
    """
)


# ============================================================
# TOP KPIs
# ============================================================

st.subheader("📌 Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        f"{summary['total_customers']:,}"
    )

with col2:
    st.metric(
        "Total Defaults",
        f"{summary['total_defaults']:,}"
    )

with col3:
    st.metric(
        "Overall Default Rate",
        f"{summary['default_rate']:.2f}%"
    )

with col4:
    st.metric(
        "Total Credit Exposure",
        f"{summary['total_credit']:,.0f}"
    )


# ============================================================
# FINANCIAL KPIs
# ============================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Income",
        f"{summary['average_income']:,.0f}"
    )

with col2:
    st.metric(
        "Average Credit",
        f"{summary['average_credit']:,.0f}"
    )

with col3:
    st.metric(
        "Average Annuity",
        f"{summary['average_annuity']:,.0f}"
    )

with col4:
    st.metric(
        "Total Annuity",
        f"{summary['total_annuity']:,.0f}"
    )


# ============================================================
# RISK OVERVIEW
# ============================================================

st.divider()

st.subheader("🎯 Portfolio Risk Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "High + Very High Risk",
        f"{risk_metrics['high_risk_customers']:,}"
    )

with col2:
    st.metric(
        "High-Risk Share",
        f"{risk_metrics['high_risk_share']:.2f}%"
    )

with col3:
    st.metric(
        "High-Risk Default Rate",
        f"{risk_metrics['high_risk_default_rate']:.2f}%"
    )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.subheader("📈 Risk Category Distribution")

fig_risk = px.bar(
    risk_distribution,
    x="RISK_CATEGORY",
    y="portfolio_share",
    text="portfolio_share",
    hover_data=[
        "customers",
        "defaults",
        "default_rate"
    ],
    title="Portfolio Share by Risk Category"
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_risk.update_xaxes(
    title="Risk Category"
)

fig_risk.update_yaxes(
    title="Portfolio Share (%)"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# RISK DEFAULT RATE
# ============================================================

fig_default = px.line(
    risk_distribution,
    x="RISK_CATEGORY",
    y="default_rate",
    markers=True,
    text="default_rate",
    title="Observed Default Rate Across Risk Categories"
)

fig_default.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="top center"
)

fig_default.update_xaxes(
    title="Risk Category"
)

fig_default.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ============================================================
# CONTRACT MIX
# ============================================================

st.divider()

st.subheader("📄 Contract Portfolio")

col1, col2 = st.columns(2)

with col1:

    fig_contract_share = px.pie(
        contract_summary,
        names="NAME_CONTRACT_TYPE",
        values="customers",
        hole=0.45,
        title="Customer Distribution by Contract Type"
    )

    st.plotly_chart(
        fig_contract_share,
        use_container_width=True
    )


with col2:

    fig_contract_default = px.bar(
        contract_summary,
        x="NAME_CONTRACT_TYPE",
        y="default_rate",
        text="default_rate",
        title="Default Rate by Contract Type"
    )

    fig_contract_default.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_contract_default.update_yaxes(
        title="Default Rate (%)"
    )

    st.plotly_chart(
        fig_contract_default,
        use_container_width=True
    )


# ============================================================
# CREDIT EXPOSURE
# ============================================================

st.divider()

st.subheader("💰 Credit Exposure by Contract Type")

credit_long = credit_exposure.melt(
    id_vars="NAME_CONTRACT_TYPE",
    value_vars=[
        "total_credit",
        "total_annuity"
    ],
    var_name="metric",
    value_name="amount"
)

credit_long["metric"] = credit_long["metric"].map(
    {
        "total_credit": "Total Credit",
        "total_annuity": "Total Annuity"
    }
)

fig_exposure = px.bar(
    credit_long,
    x="NAME_CONTRACT_TYPE",
    y="amount",
    color="metric",
    barmode="group",
    title="Total Credit and Annuity Exposure"
)

fig_exposure.update_yaxes(
    title="Amount"
)

st.plotly_chart(
    fig_exposure,
    use_container_width=True
)


# ============================================================
# INCOME VS CREDIT
# ============================================================

st.divider()

st.subheader("💵 Income vs Credit Profile")

income_long = income_credit.melt(
    id_vars="INCOME_GROUP",
    value_vars=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY"
    ],
    var_name="metric",
    value_name="average_value"
)

income_long["metric"] = income_long["metric"].map(
    {
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit",
        "AMT_ANNUITY": "Annuity"
    }
)

fig_income = px.bar(
    income_long,
    x="INCOME_GROUP",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Financial Metrics by Income Group"
)

fig_income.update_xaxes(
    title="Income Group"
)

fig_income.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Executive Portfolio Insights")

highest_risk = risk_distribution.loc[
    risk_distribution["default_rate"].idxmax()
]

largest_risk_segment = risk_distribution.loc[
    risk_distribution["customers"].idxmax()
]

largest_contract = contract_summary.loc[
    contract_summary["customers"].idxmax()
]

col1, col2, col3 = st.columns(3)

with col1:
    st.warning(
        f"""
        **Highest Observed Risk**

        {highest_risk['RISK_CATEGORY']}

        Default Rate:
        **{highest_risk['default_rate']:.2f}%**

        Customers:
        **{highest_risk['customers']:,}**
        """
    )

with col2:
    st.info(
        f"""
        **Largest Risk Segment**

        {largest_risk_segment['RISK_CATEGORY']}

        Portfolio Share:
        **{largest_risk_segment['portfolio_share']:.2f}%**

        Customers:
        **{largest_risk_segment['customers']:,}**
        """
    )

with col3:
    st.info(
        f"""
        **Largest Contract Segment**

        {largest_contract['NAME_CONTRACT_TYPE']}

        Portfolio Share:
        **{largest_contract['portfolio_share']:.2f}%**

        Default Rate:
        **{largest_contract['default_rate']:.2f}%**
        """
    )


# ============================================================
# FINAL RISK MESSAGE
# ============================================================

st.divider()

st.subheader("🚨 Portfolio Risk Signal")

st.warning(
    f"""
    **{risk_metrics['high_risk_share']:.2f}%** of customers fall into
    the High or Very High Risk categories.

    This segment has an observed default rate of
    **{risk_metrics['high_risk_default_rate']:.2f}%**.

    The Very High Risk segment alone contains
    **{risk_metrics['very_high_risk_customers']:,} customers**
    with an observed default rate of
    **{risk_metrics['very_high_risk_default_rate']:.2f}%**.
    """
)


st.caption(
    "This page summarizes observed historical patterns in the "
    "dataset. Risk segments are analytical classifications and "
    "should not be interpreted as causal or as individual credit "
    "approval decisions."
)