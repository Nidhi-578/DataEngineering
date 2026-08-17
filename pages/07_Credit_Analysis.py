import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    prepare_customer_data,
    credit_statistics,
    credit_group_distribution,
    default_rate_by_credit_group,
    credit_income_summary,
    credit_income_risk,
)


st.set_page_config(
    page_title="Credit Analysis",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading credit analysis..."):
    df = load_data()
df = prepare_customer_data(df)


# ============================================================
# HEADER
# ============================================================

st.title("💳 Credit Analysis")

st.markdown(
    """
    Analyze loan credit amounts, credit distribution,
    credit-to-income ratios, and credit-related default risk.
    """
)


# ============================================================
# CREDIT KPIs
# ============================================================

stats = credit_statistics(df)

ratio_stats = credit_income_summary(df)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Credit",
        f"₹{stats['total_credit']:,.0f}"
    )

with col2:
    st.metric(
        "Average Credit",
        f"₹{stats['average_credit']:,.0f}"
    )

with col3:
    st.metric(
        "Median Credit",
        f"₹{stats['median_credit']:,.0f}"
    )

with col4:
    st.metric(
        "Average Credit / Income",
        f"{ratio_stats['average_ratio']:.2f}x"
    )


# ============================================================
# ADDITIONAL CREDIT METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Minimum Credit",
        f"₹{stats['minimum_credit']:,.0f}"
    )

with col2:
    st.metric(
        "Maximum Credit",
        f"₹{stats['maximum_credit']:,.0f}"
    )

with col3:
    st.metric(
        "Median Credit / Income",
        f"{ratio_stats['median_ratio']:.2f}x"
    )

with col4:
    st.metric(
        "Maximum Credit / Income",
        f"{ratio_stats['maximum_ratio']:.2f}x"
    )


# ============================================================
# CREDIT DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Credit Amount Distribution")

credit_groups = credit_group_distribution(df)

fig_distribution = px.bar(
    credit_groups,
    x="CREDIT_GROUP",
    y="customers",
    text="customers",
    title="Customers by Credit Amount Group"
)

fig_distribution.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_distribution.update_xaxes(
    title="Credit Group"
)

fig_distribution.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# CREDIT HISTOGRAM
# ============================================================

st.subheader("📈 Credit Amount Distribution")

fig_hist = px.histogram(
    df,
    x="AMT_CREDIT",
    nbins=60,
    title="Distribution of Loan Credit Amount"
)

fig_hist.update_xaxes(
    title="Credit Amount"
)

fig_hist.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY CREDIT GROUP
# ============================================================

st.divider()

st.subheader("⚠️ Default Rate by Credit Group")

credit_risk = default_rate_by_credit_group(df)

fig_credit_risk = px.bar(
    credit_risk,
    x="CREDIT_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Credit Amount Group"
)

fig_credit_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_credit_risk.update_xaxes(
    title="Credit Group"
)

fig_credit_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_credit_risk,
    use_container_width=True
)


# ============================================================
# CREDIT VS INCOME
# ============================================================

st.subheader("💰 Credit vs Income")

scatter_df = df[
    [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "TARGET"
    ]
].dropna()

if len(scatter_df) > 10000:
    scatter_df = scatter_df.sample(
        10000,
        random_state=42
    )

scatter_df["Status"] = scatter_df["TARGET"].map(
    {
        0: "Non-Default",
        1: "Default"
    }
)

fig_scatter = px.scatter(
    scatter_df,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="Status",
    opacity=0.6,
    title="Credit Amount vs Customer Income"
)

fig_scatter.update_xaxes(
    title="Income"
)

fig_scatter.update_yaxes(
    title="Credit Amount"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ============================================================
# CREDIT-TO-INCOME RISK
# ============================================================

st.divider()

st.subheader("📐 Credit-to-Income Risk")

ratio_data = credit_income_risk(df)

fig_ratio = px.bar(
    ratio_data,
    x="RATIO_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "applications",
        "defaults"
    ],
    title="Default Rate by Credit-to-Income Ratio"
)

fig_ratio.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_ratio.update_xaxes(
    title="Credit-to-Income Ratio"
)

fig_ratio.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_ratio,
    use_container_width=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Credit Insights")

highest_risk_credit = credit_risk.loc[
    credit_risk["default_rate"].idxmax()
]

lowest_risk_credit = credit_risk.loc[
    credit_risk["default_rate"].idxmin()
]

highest_ratio_risk = ratio_data.loc[
    ratio_data["default_rate"].idxmax()
]

col1, col2, col3 = st.columns(3)

with col1:
    st.warning(
        f"""
        **Highest Credit-Group Risk**

        {highest_risk_credit['CREDIT_GROUP']}

        Default Rate:
        **{highest_risk_credit['default_rate']:.2f}%**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Credit-Group Risk**

        {lowest_risk_credit['CREDIT_GROUP']}

        Default Rate:
        **{lowest_risk_credit['default_rate']:.2f}%**
        """
    )

with col3:
    st.info(
        f"""
        **Highest Ratio Risk**

        {highest_ratio_risk['RATIO_GROUP']}

        Default Rate:
        **{highest_ratio_risk['default_rate']:.2f}%**
        """
    )


st.caption(
    "Credit and default relationships shown here are descriptive "
    "patterns from the dataset and are not causal conclusions."
)