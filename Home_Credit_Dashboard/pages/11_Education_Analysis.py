import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    education_distribution,
    education_default_summary,
    education_financial_summary,
    education_income_risk,
)


st.set_page_config(
    page_title="Education Analysis",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading education analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Education Analysis")

st.markdown(
    """
    Analyze applicant education levels, financial characteristics,
    and observed default risk across education and income segments.
    """
)


# ============================================================
# EDUCATION DISTRIBUTION
# ============================================================

education_data = education_distribution(df)

total_customers = education_data["customers"].sum()
most_common_education = education_data.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Most Common Education",
        most_common_education["education"]
    )


st.divider()

st.subheader("📊 Education Distribution")

fig_distribution = px.bar(
    education_data,
    x="education",
    y="customers",
    text="customers",
    title="Customers by Education Level"
)

fig_distribution.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_distribution.update_xaxes(
    title="Education Level",
    tickangle=-25
)

fig_distribution.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY EDUCATION
# ============================================================

st.subheader("⚠️ Default Rate by Education")

education_risk = education_default_summary(df)

fig_risk = px.bar(
    education_risk,
    x="NAME_EDUCATION_TYPE",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Education Level"
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_risk.update_xaxes(
    title="Education Level",
    tickangle=-25
)

fig_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# EDUCATION FINANCIAL PROFILE
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Education")

financial_data = education_financial_summary(df)

financial_long = financial_data.melt(
    id_vars="NAME_EDUCATION_TYPE",
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
    x="NAME_EDUCATION_TYPE",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Education"
)

fig_financial.update_xaxes(
    title="Education Level",
    tickangle=-25
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# EDUCATION × INCOME TYPE
# ============================================================

st.divider()

st.subheader("🔎 Education × Income Type Risk")

education_income = education_income_risk(df)

fig_heatmap = px.density_heatmap(
    education_income,
    x="NAME_INCOME_TYPE",
    y="NAME_EDUCATION_TYPE",
    z="default_rate",
    text_auto=".2f",
    title="Default Rate: Education vs Income Type",
    hover_data=[
        "customers",
        "defaults"
    ]
)

fig_heatmap.update_xaxes(
    title="Income Type"
)

fig_heatmap.update_yaxes(
    title="Education Level"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# ============================================================
# EDUCATION RISK TABLE
# ============================================================

st.subheader("📋 Education Risk Summary")

display_risk = education_risk.copy()

display_risk["default_rate"] = (
    display_risk["default_rate"].round(2)
)

st.dataframe(
    display_risk,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# TOP EDUCATION × INCOME SEGMENTS
# ============================================================

st.subheader("🏆 Highest-Risk Education × Income Segments")

top_segments = (
    education_income[
        education_income["customers"] >= 50
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

st.subheader("💡 Education Insights")

meaningful_risk = education_risk[
    education_risk["customers"] >= 50
]

highest_risk = meaningful_risk.loc[
    meaningful_risk["default_rate"].idxmax()
]

lowest_risk = meaningful_risk.loc[
    meaningful_risk["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Observed Education Risk**

        {highest_risk['NAME_EDUCATION_TYPE']}

        Default Rate:
        **{highest_risk['default_rate']:.2f}%**

        Customers:
        **{highest_risk['customers']:,}**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Observed Education Risk**

        {lowest_risk['NAME_EDUCATION_TYPE']}

        Default Rate:
        **{lowest_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_risk['customers']:,}**
        """
    )


st.caption(
    "Default rates describe observed patterns in the dataset. "
    "Small segments should be interpreted cautiously and these "
    "relationships should not be treated as causal."
)