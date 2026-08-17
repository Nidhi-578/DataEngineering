import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    annuity_income_summary,
    annuity_burden_distribution,
    default_rate_by_annuity_burden,
    high_annuity_burden_summary,
)


st.set_page_config(
    page_title="Annuity Burden",
    page_icon="📐",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading annuity burden analysis..."):
    df = load_data()


st.title("📐 Annuity Burden Analysis")

st.markdown(
    """
    Analyze the repayment burden of loan applicants by comparing
    annual loan annuity with annual customer income.
    """
)


# ============================================================
# KPI SECTION
# ============================================================

ratio_summary = annuity_income_summary(df)
high_burden = high_annuity_burden_summary(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Annuity / Income",
        f"{ratio_summary['average_ratio']:.2%}"
    )

with col2:
    st.metric(
        "Median Annuity / Income",
        f"{ratio_summary['median_ratio']:.2%}"
    )

with col3:
    st.metric(
        "High-Burden Customers",
        f"{high_burden['customers']:,}"
    )

with col4:
    st.metric(
        "High-Burden Default Rate",
        f"{high_burden['default_rate']:.2f}%"
    )


# ============================================================
# BURDEN DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Annuity Burden Distribution")

burden_distribution = annuity_burden_distribution(df)

fig_distribution = px.bar(
    burden_distribution,
    x="ANNUITY_BURDEN",
    y="customers",
    text="customers",
    title="Customers by Annuity-to-Income Burden"
)

fig_distribution.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_distribution.update_xaxes(
    title="Annuity-to-Income Burden"
)

fig_distribution.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE
# ============================================================

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
    title="Default Rate by Annuity Burden"
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
# INCOME VS ANNUITY BURDEN
# ============================================================

st.divider()

st.subheader("💰 Income vs Annuity Burden")

plot_df = df[
    [
        "AMT_INCOME_TOTAL",
        "AMT_ANNUITY",
        "TARGET"
    ]
].dropna()

if len(plot_df) > 10000:
    plot_df = plot_df.sample(
        10000,
        random_state=42
    )

plot_df["ANNUITY_INCOME_RATIO"] = (
    plot_df["AMT_ANNUITY"] /
    plot_df["AMT_INCOME_TOTAL"]
)

plot_df["Status"] = plot_df["TARGET"].map(
    {
        0: "Non-Default",
        1: "Default"
    }
)

fig_scatter = px.scatter(
    plot_df,
    x="AMT_INCOME_TOTAL",
    y="ANNUITY_INCOME_RATIO",
    color="Status",
    opacity=0.6,
    title="Income vs Annuity-to-Income Ratio"
)

fig_scatter.update_xaxes(
    title="Income"
)

fig_scatter.update_yaxes(
    title="Annuity / Income Ratio"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ============================================================
# HIGH BURDEN SEGMENT
# ============================================================

st.divider()

st.subheader("🚨 High Annuity-Burden Segment")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        f"{high_burden['customers']:,}"
    )

with col2:
    st.metric(
        "Defaults",
        f"{high_burden['defaults']:,}"
    )

with col3:
    st.metric(
        "Default Rate",
        f"{high_burden['default_rate']:.2f}%"
    )

with col4:
    st.metric(
        "Average Burden",
        f"{high_burden['average_ratio']:.2%}"
    )


st.info(
    f"""
    Customers with an annuity-to-income ratio of **30% or higher**
    have an average income of approximately
    **₹{high_burden['average_income']:,.0f}** and an average
    annuity of approximately **₹{high_burden['average_annuity']:,.0f}**.
    """
)


# ============================================================
# BURDEN TABLE
# ============================================================

st.subheader("📋 Annuity Burden Risk Table")

display_df = burden_risk.copy()

display_df["default_rate"] = (
    display_df["default_rate"].round(2)
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Annuity Burden Insights")

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
        **Highest Observed Burden Risk**

        Burden:
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
        **Lowest Observed Burden Risk**

        Burden:
        **{lowest_risk['ANNUITY_BURDEN']}**

        Default Rate:
        **{lowest_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_risk['customers']:,}**
        """
    )


st.caption(
    "Annuity burden and default rates describe observed patterns "
    "in the dataset and should not be interpreted as causal "
    "relationships."
)