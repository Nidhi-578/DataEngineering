import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    contract_type_summary,
    contract_financial_summary,
    contract_ratio_summary,
    contract_income_risk,
)


st.set_page_config(
    page_title="Contract Analysis",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading contract analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("📄 Contract Type Analysis")

st.markdown(
    """
    Compare Cash loans and Revolving loans across application
    volume, default risk, financial characteristics, and
    credit-to-income ratios.
    """
)


# ============================================================
# SUMMARY
# ============================================================

contract_data = contract_type_summary(df)

cash_row = contract_data[
    contract_data["NAME_CONTRACT_TYPE"] == "Cash loans"
]

revolving_row = contract_data[
    contract_data["NAME_CONTRACT_TYPE"] == "Revolving loans"
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Applications",
        f"{contract_data['customers'].sum():,}"
    )

with col2:
    st.metric(
        "Cash Loans",
        f"{int(cash_row['customers'].sum()):,}"
    )

with col3:
    st.metric(
        "Revolving Loans",
        f"{int(revolving_row['customers'].sum()):,}"
    )

with col4:
    st.metric(
        "Overall Default Rate",
        f"{df['TARGET'].mean() * 100:.2f}%"
    )


# ============================================================
# CONTRACT DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Contract Type Distribution")

fig_distribution = px.pie(
    contract_data,
    names="NAME_CONTRACT_TYPE",
    values="customers",
    hole=0.45,
    title="Applications by Contract Type"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE
# ============================================================

st.subheader("⚠️ Default Rate by Contract Type")

fig_default = px.bar(
    contract_data,
    x="NAME_CONTRACT_TYPE",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Contract Type"
)

fig_default.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_default.update_xaxes(
    title="Contract Type"
)

fig_default.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ============================================================
# FINANCIAL COMPARISON
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Contract Type")

financial_data = contract_financial_summary(df)

financial_long = financial_data.melt(
    id_vars="NAME_CONTRACT_TYPE",
    value_vars=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY"
    ],
    var_name="metric",
    value_name="average_value"
)

financial_long["metric"] = financial_long["metric"].map(
    {
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit",
        "AMT_ANNUITY": "Annuity"
    }
)

fig_financial = px.bar(
    financial_long,
    x="NAME_CONTRACT_TYPE",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity"
)

fig_financial.update_xaxes(
    title="Contract Type"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# CREDIT / INCOME RATIO
# ============================================================

st.subheader("📐 Credit-to-Income Ratio")

ratio_data = contract_ratio_summary(df)

col1, col2 = st.columns(2)

with col1:

    fig_ratio = px.bar(
        ratio_data,
        x="NAME_CONTRACT_TYPE",
        y="average_ratio",
        text="average_ratio",
        title="Average Credit-to-Income Ratio"
    )

    fig_ratio.update_traces(
        texttemplate="%{text:.2f}x",
        textposition="outside"
    )

    fig_ratio.update_xaxes(
        title="Contract Type"
    )

    fig_ratio.update_yaxes(
        title="Credit / Income"
    )

    st.plotly_chart(
        fig_ratio,
        use_container_width=True
    )

with col2:

    ratio_display = ratio_data.copy()

    ratio_display["average_ratio"] = (
        ratio_display["average_ratio"].round(2)
    )

    ratio_display["median_ratio"] = (
        ratio_display["median_ratio"].round(2)
    )

    ratio_display["minimum_ratio"] = (
        ratio_display["minimum_ratio"].round(2)
    )

    ratio_display["maximum_ratio"] = (
        ratio_display["maximum_ratio"].round(2)
    )

    st.dataframe(
        ratio_display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CONTRACT × INCOME RISK
# ============================================================

st.divider()

st.subheader("🔎 Contract Type × Income Group Risk")

income_risk = contract_income_risk(df)

fig_heatmap = px.density_heatmap(
    income_risk,
    x="INCOME_GROUP",
    y="NAME_CONTRACT_TYPE",
    z="default_rate",
    text_auto=".2f",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Contract Type and Income Group"
)

fig_heatmap.update_xaxes(
    title="Income Group"
)

fig_heatmap.update_yaxes(
    title="Contract Type"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# ============================================================
# RISK TABLE
# ============================================================

st.subheader("📋 Contract Risk Summary")

display_contract = contract_data.copy()

display_contract["default_rate"] = (
    display_contract["default_rate"].round(2)
)

st.dataframe(
    display_contract,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HIGHEST-RISK SEGMENTS
# ============================================================

st.subheader("🏆 Contract × Income Risk Segments")

top_segments = (
    income_risk[
        income_risk["customers"] >= 50
    ]
    .sort_values(
        "default_rate",
        ascending=False
    )
    .head(10)
)

top_segments["default_rate"] = (
    top_segments["default_rate"].round(2)
)

st.dataframe(
    top_segments,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Contract Insights")

meaningful_segments = income_risk[
    income_risk["customers"] >= 50
]

highest_segment = meaningful_segments.loc[
    meaningful_segments["default_rate"].idxmax()
]

lowest_segment = meaningful_segments.loc[
    meaningful_segments["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Observed Contract × Income Risk**

        Contract:
        **{highest_segment['NAME_CONTRACT_TYPE']}**

        Income:
        **{highest_segment['INCOME_GROUP']}**

        Default Rate:
        **{highest_segment['default_rate']:.2f}%**

        Customers:
        **{highest_segment['customers']:,}**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Observed Contract × Income Risk**

        Contract:
        **{lowest_segment['NAME_CONTRACT_TYPE']}**

        Income:
        **{lowest_segment['INCOME_GROUP']}**

        Default Rate:
        **{lowest_segment['default_rate']:.2f}%**

        Customers:
        **{lowest_segment['customers']:,}**
        """
    )


st.caption(
    "Default rates describe observed patterns in the dataset. "
    "Small segments should be interpreted cautiously and these "
    "relationships should not be treated as causal."
)