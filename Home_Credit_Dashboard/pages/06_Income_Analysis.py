import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    prepare_customer_data,
    income_summary,
    income_group_distribution,
    default_rate_by_income_group,
    income_type_summary,
    income_credit_summary,
)


st.set_page_config(
    page_title="Income Analysis",
    page_icon="💰",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading income analysis..."):
    df = load_data()

df = prepare_customer_data(df)


st.title("💰 Income Analysis")

st.markdown(
    """
    Analyze applicant income levels, income groups, income
    sources, financial characteristics, and default risk.
    """
)


# ============================================================
# KPIs
# ============================================================

summary = income_summary(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Income",
        f"₹{summary['average_income']:,.0f}"
    )

with col2:
    st.metric(
        "Median Income",
        f"₹{summary['median_income']:,.0f}"
    )

with col3:
    st.metric(
        "Minimum Income",
        f"₹{summary['minimum_income']:,.0f}"
    )

with col4:
    st.metric(
        "Maximum Income",
        f"₹{summary['maximum_income']:,.0f}"
    )


# ============================================================
# INCOME GROUP DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Income Group Distribution")

group_data = income_group_distribution(df)

fig_groups = px.bar(
    group_data,
    x="INCOME_GROUP",
    y="customers",
    text="customers",
    title="Customers by Income Group"
)

fig_groups.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_groups.update_xaxes(
    title="Income Group"
)

fig_groups.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_groups,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY INCOME GROUP
# ============================================================

st.subheader("⚠️ Default Rate by Income Group")

risk_group = default_rate_by_income_group(df)

fig_risk_group = px.bar(
    risk_group,
    x="INCOME_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Income Group"
)

fig_risk_group.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_risk_group.update_xaxes(
    title="Income Group"
)

fig_risk_group.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_risk_group,
    use_container_width=True
)


# ============================================================
# INCOME TYPE
# ============================================================

st.divider()

st.subheader("💼 Income Type Analysis")

income_type = income_type_summary(df)

fig_income_type = px.bar(
    income_type,
    x="default_rate",
    y="NAME_INCOME_TYPE",
    orientation="h",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Income Type"
)

fig_income_type.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_income_type.update_xaxes(
    title="Default Rate (%)"
)

fig_income_type.update_yaxes(
    title="Income Type"
)

st.plotly_chart(
    fig_income_type,
    use_container_width=True
)


# ============================================================
# FINANCIAL CHARACTERISTICS
# ============================================================

st.subheader("💳 Financial Characteristics by Income Group")

financial_data = income_credit_summary(df)

financial_long = financial_data.melt(
    id_vars="INCOME_GROUP",
    value_vars=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY"
    ],
    var_name="metric",
    value_name="average_value"
)

financial_long["metric"] = (
    financial_long["metric"]
    .map(
        {
            "AMT_INCOME_TOTAL": "Income",
            "AMT_CREDIT": "Credit",
            "AMT_ANNUITY": "Annuity"
        }
    )
)

fig_financial = px.bar(
    financial_long,
    x="INCOME_GROUP",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Income Group"
)

fig_financial.update_xaxes(
    title="Income Group"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# INCOME DISTRIBUTION
# ============================================================

st.subheader("📈 Income Distribution")

fig_hist = px.histogram(
    df,
    x="AMT_INCOME_TOTAL",
    nbins=50,
    title="Applicant Income Distribution"
)

fig_hist.update_xaxes(
    title="Income"
)

fig_hist.update_yaxes(
    title="Number of Customers"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)


# ============================================================
# INCOME VS DEFAULT
# ============================================================

st.subheader("⚠️ Income vs Default Status")

sample_df = df[
    [
        "AMT_INCOME_TOTAL",
        "TARGET"
    ]
].dropna()

if len(sample_df) > 10000:
    sample_df = sample_df.sample(
        10000,
        random_state=42
    )

sample_df["Status"] = sample_df["TARGET"].map(
    {
        0: "Non-Default",
        1: "Default"
    }
)

fig_income_default = px.box(
    sample_df,
    x="Status",
    y="AMT_INCOME_TOTAL",
    title="Income Distribution by Default Status"
)

fig_income_default.update_xaxes(
    title="Status"
)

fig_income_default.update_yaxes(
    title="Income"
)

st.plotly_chart(
    fig_income_default,
    use_container_width=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Income Insights")

highest_risk_group = risk_group.loc[
    risk_group["default_rate"].idxmax()
]

lowest_risk_group = risk_group.loc[
    risk_group["default_rate"].idxmin()
]

highest_income_type = income_type.loc[
    income_type["default_rate"].idxmax()
]

col1, col2, col3 = st.columns(3)

with col1:
    st.warning(
        f"""
        **Highest Income-Group Default Rate**

        {highest_risk_group['INCOME_GROUP']}

        **{highest_risk_group['default_rate']:.2f}%**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Income-Group Default Rate**

        {lowest_risk_group['INCOME_GROUP']}

        **{lowest_risk_group['default_rate']:.2f}%**
        """
    )

with col3:
    st.info(
        f"""
        **Highest Income-Type Default Rate**

        {highest_income_type['NAME_INCOME_TYPE']}

        **{highest_income_type['default_rate']:.2f}%**
        """
    )


st.caption(
    "Default rates describe observed patterns in the dataset "
    "and should not be interpreted as causal relationships."
)