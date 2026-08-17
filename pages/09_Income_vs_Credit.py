import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    prepare_customer_data,
    income_credit_segment_summary,
    high_credit_low_income_summary,
    credit_income_risk,
)


st.set_page_config(
    page_title="Income vs Credit",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading income vs credit analysis..."):
    df = load_data()

df = prepare_customer_data(df)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Income vs Credit Analysis")

st.markdown(
    """
    Analyze the relationship between customer income,
    loan credit amount, credit-to-income ratio, and
    observed default risk.
    """
)


# ============================================================
# KEY METRICS
# ============================================================

high_risk_segment = high_credit_low_income_summary(df)

average_ratio = (
    df["AMT_CREDIT"] /
    df["AMT_INCOME_TOTAL"]
).mean()

median_ratio = (
    df["AMT_CREDIT"] /
    df["AMT_INCOME_TOTAL"]
).median()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Credit / Income",
        f"{average_ratio:.2f}x"
    )

with col2:
    st.metric(
        "Median Credit / Income",
        f"{median_ratio:.2f}x"
    )

with col3:
    st.metric(
        "High Credit / Income Customers",
        f"{high_risk_segment['customers']:,}"
    )

with col4:
    st.metric(
        "High Ratio Default Rate",
        f"{high_risk_segment['default_rate']:.2f}%"
    )


# ============================================================
# INCOME VS CREDIT SCATTER
# ============================================================

st.divider()

st.subheader("💰 Income vs Credit Amount")

scatter_df = df[
    [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "TARGET",
        "INCOME_GROUP"
    ]
].dropna()

if len(scatter_df) > 15000:
    scatter_df = scatter_df.sample(
        15000,
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
    hover_data=["INCOME_GROUP"],
    opacity=0.55,
    title="Loan Credit Amount vs Customer Income"
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
# CREDIT-INCOME RATIO DISTRIBUTION
# ============================================================

st.subheader("📐 Credit-to-Income Ratio Distribution")

ratio_df = df.copy()

ratio_df["CREDIT_INCOME_RATIO"] = (
    ratio_df["AMT_CREDIT"] /
    ratio_df["AMT_INCOME_TOTAL"]
)

fig_ratio = px.histogram(
    ratio_df,
    x="CREDIT_INCOME_RATIO",
    nbins=60,
    title="Distribution of Credit-to-Income Ratio"
)

fig_ratio.update_xaxes(
    title="Credit / Income Ratio"
)

fig_ratio.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_ratio,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY RATIO
# ============================================================

st.subheader("⚠️ Default Rate by Credit-to-Income Ratio")

ratio_risk = credit_income_risk(df)

fig_ratio_risk = px.bar(
    ratio_risk,
    x="RATIO_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "applications",
        "defaults"
    ],
    title="Default Rate by Credit-to-Income Ratio"
)

fig_ratio_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_ratio_risk.update_xaxes(
    title="Credit-to-Income Ratio"
)

fig_ratio_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_ratio_risk,
    use_container_width=True
)


# ============================================================
# INCOME × CREDIT SEGMENTS
# ============================================================

st.divider()

st.subheader("🔎 Income Group × Credit Group Risk")

segment_data = income_credit_segment_summary(df)

fig_segment = px.density_heatmap(
    segment_data,
    x="CREDIT_GROUP",
    y="INCOME_GROUP",
    z="default_rate",
    text_auto=".2f",
    title="Default Rate Heatmap: Income vs Credit",
    hover_data=[
        "applications",
        "defaults"
    ]
)

fig_segment.update_xaxes(
    title="Credit Group"
)

fig_segment.update_yaxes(
    title="Income Group"
)

st.plotly_chart(
    fig_segment,
    use_container_width=True
)


# ============================================================
# CUSTOMER COUNT HEATMAP
# ============================================================

st.subheader("👥 Customer Distribution: Income vs Credit")

fig_count = px.density_heatmap(
    segment_data,
    x="CREDIT_GROUP",
    y="INCOME_GROUP",
    z="applications",
    text_auto=True,
    title="Customer Count by Income and Credit Group"
)

fig_count.update_xaxes(
    title="Credit Group"
)

fig_count.update_yaxes(
    title="Income Group"
)

st.plotly_chart(
    fig_count,
    use_container_width=True
)


# ============================================================
# HIGH CREDIT / LOW INCOME SEGMENT
# ============================================================

st.divider()

st.subheader("🚨 High Credit-to-Income Segment")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        f"{high_risk_segment['customers']:,}"
    )

with col2:
    st.metric(
        "Defaults",
        f"{high_risk_segment['defaults']:,}"
    )

with col3:
    st.metric(
        "Default Rate",
        f"{high_risk_segment['default_rate']:.2f}%"
    )

with col4:
    st.metric(
        "Average Ratio",
        f"{high_risk_segment['average_ratio']:.2f}x"
    )


st.info(
    f"""
    Customers with a credit-to-income ratio of **6x or higher**
    have an average income of approximately
    **₹{high_risk_segment['average_income']:,.0f}** and an
    average credit amount of approximately
    **₹{high_risk_segment['average_credit']:,.0f}**.
    """
)


# ============================================================
# TOP RISK SEGMENTS
# ============================================================

st.subheader("🏆 Highest-Risk Income × Credit Segments")

top_segments = (
    segment_data[
        segment_data["applications"] >= 50
    ]
    .sort_values(
        "default_rate",
        ascending=False
    )
    .head(10)
)

display_segments = top_segments.copy()

display_segments["default_rate"] = (
    display_segments["default_rate"]
    .round(2)
)

st.dataframe(
    display_segments,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Income vs Credit Insights")

highest_segment = (
    segment_data[
        segment_data["applications"] >= 50
    ]
    .sort_values(
        "default_rate",
        ascending=False
    )
    .iloc[0]
)


col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Meaningful Income × Credit Risk**

        Income Group:
        **{highest_segment['INCOME_GROUP']}**

        Credit Group:
        **{highest_segment['CREDIT_GROUP']}**

        Default Rate:
        **{highest_segment['default_rate']:.2f}%**

        Customers:
        **{highest_segment['applications']:,}**
        """
    )

with col2:
    st.info(
        f"""
        **High Credit-to-Income Segment**

        Customers:
        **{high_risk_segment['customers']:,}**

        Average Ratio:
        **{high_risk_segment['average_ratio']:.2f}x**

        Default Rate:
        **{high_risk_segment['default_rate']:.2f}%**
        """
    )


st.caption(
    "These analyses describe observed relationships in the "
    "dataset. They should not be interpreted as causal "
    "relationships or individual credit decisions."
)