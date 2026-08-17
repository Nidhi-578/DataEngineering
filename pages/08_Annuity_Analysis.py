import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    annuity_summary,
    annuity_income_summary,
    annuity_burden_distribution,
    default_rate_by_annuity_burden,
)


st.set_page_config(
    page_title="Annuity Analysis",
    page_icon="🧾",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading annuity analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🧾 Annuity Analysis")

st.markdown(
    """
    Analyze loan annuity amounts, annuity-to-income burden,
    and the relationship between repayment burden and
    observed default risk.
    """
)


# ============================================================
# KPI CARDS
# ============================================================

summary = annuity_summary(df)
ratio_summary = annuity_income_summary(df)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Annuity",
        f"₹{summary['total_annuity']:,.0f}"
    )

with col2:
    st.metric(
        "Average Annuity",
        f"₹{summary['average_annuity']:,.0f}"
    )

with col3:
    st.metric(
        "Median Annuity",
        f"₹{summary['median_annuity']:,.0f}"
    )

with col4:
    st.metric(
        "Average Annuity / Income",
        f"{ratio_summary['average_ratio']:.2%}"
    )


# ============================================================
# ADDITIONAL METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Minimum Annuity",
        f"₹{summary['minimum_annuity']:,.0f}"
    )

with col2:
    st.metric(
        "Maximum Annuity",
        f"₹{summary['maximum_annuity']:,.0f}"
    )

with col3:
    st.metric(
        "Median Annuity / Income",
        f"{ratio_summary['median_ratio']:.2%}"
    )

with col4:
    st.metric(
        "Maximum Annuity / Income",
        f"{ratio_summary['maximum_ratio']:.2%}"
    )


# ============================================================
# ANNUITY DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Annuity Distribution")

fig_hist = px.histogram(
    df,
    x="AMT_ANNUITY",
    nbins=60,
    title="Distribution of Loan Annuity"
)

fig_hist.update_xaxes(
    title="Annuity Amount"
)

fig_hist.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)


# ============================================================
# ANNUITY BURDEN DISTRIBUTION
# ============================================================

st.subheader("📐 Annuity-to-Income Burden")

burden_distribution = annuity_burden_distribution(df)

fig_burden = px.bar(
    burden_distribution,
    x="ANNUITY_BURDEN",
    y="customers",
    text="customers",
    title="Customers by Annuity-to-Income Burden"
)

fig_burden.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_burden.update_xaxes(
    title="Annuity Burden"
)

fig_burden.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_burden,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY BURDEN
# ============================================================

st.divider()

st.subheader("⚠️ Default Rate by Annuity Burden")

burden_risk = default_rate_by_annuity_burden(df)

fig_risk = px.bar(
    burden_risk,
    x="ANNUITY_BURDEN",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Annuity-to-Income Burden"
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_risk.update_xaxes(
    title="Annuity Burden"
)

fig_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# INCOME VS ANNUITY
# ============================================================

st.subheader("💰 Income vs Annuity")

scatter_df = df[
    [
        "AMT_INCOME_TOTAL",
        "AMT_ANNUITY",
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

fig_income_annuity = px.scatter(
    scatter_df,
    x="AMT_INCOME_TOTAL",
    y="AMT_ANNUITY",
    color="Status",
    opacity=0.6,
    title="Income vs Annuity"
)

fig_income_annuity.update_xaxes(
    title="Income"
)

fig_income_annuity.update_yaxes(
    title="Annuity"
)

st.plotly_chart(
    fig_income_annuity,
    use_container_width=True
)


# ============================================================
# CREDIT VS ANNUITY
# ============================================================

st.subheader("💳 Credit vs Annuity")

credit_annuity_df = df[
    [
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "TARGET"
    ]
].dropna()

if len(credit_annuity_df) > 10000:
    credit_annuity_df = credit_annuity_df.sample(
        10000,
        random_state=42
    )

credit_annuity_df["Status"] = (
    credit_annuity_df["TARGET"]
    .map(
        {
            0: "Non-Default",
            1: "Default"
        }
    )
)

fig_credit_annuity = px.scatter(
    credit_annuity_df,
    x="AMT_CREDIT",
    y="AMT_ANNUITY",
    color="Status",
    opacity=0.6,
    title="Credit Amount vs Annuity"
)

fig_credit_annuity.update_xaxes(
    title="Credit Amount"
)

fig_credit_annuity.update_yaxes(
    title="Annuity"
)

st.plotly_chart(
    fig_credit_annuity,
    use_container_width=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Annuity Insights")

highest_risk = burden_risk.loc[
    burden_risk["default_rate"].idxmax()
]

lowest_risk = burden_risk.loc[
    burden_risk["default_rate"].idxmin()
]


col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Observed Annuity-Burden Risk**

        Burden Group:
        **{highest_risk['ANNUITY_BURDEN']}**

        Default Rate:
        **{highest_risk['default_rate']:.2f}%**

        Customers:
        **{highest_risk['customers']:,}**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Observed Annuity-Burden Risk**

        Burden Group:
        **{lowest_risk['ANNUITY_BURDEN']}**

        Default Rate:
        **{lowest_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_risk['customers']:,}**
        """
    )


st.caption(
    "Annuity burden and default rates describe observed "
    "patterns in the dataset and should not be interpreted "
    "as causal relationships."
)