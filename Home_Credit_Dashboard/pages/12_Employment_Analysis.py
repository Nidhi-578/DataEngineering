import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    employment_summary,
    employment_group_distribution,
    default_rate_by_employment_group,
    occupation_risk_summary,
    organization_risk_summary,
    employment_financial_summary,
)


st.set_page_config(
    page_title="Employment Analysis",
    page_icon="💼",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading employment analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("💼 Employment Analysis")

st.markdown(
    """
    Analyze employment duration, occupation, organization type,
    financial characteristics, and observed default risk.
    """
)


# ============================================================
# EMPLOYMENT KPIs
# ============================================================

summary = employment_summary(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Employment",
        f"{summary['average_employment_years']:.2f} years"
    )

with col2:
    st.metric(
        "Median Employment",
        f"{summary['median_employment_years']:.2f} years"
    )

with col3:
    st.metric(
        "Minimum Employment",
        f"{summary['minimum_employment_years']:.2f} years"
    )

with col4:
    st.metric(
        "Maximum Employment",
        f"{summary['maximum_employment_years']:.2f} years"
    )


# ============================================================
# EMPLOYMENT DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Employment Duration Distribution")

employment_distribution = employment_group_distribution(df)

fig_distribution = px.bar(
    employment_distribution,
    x="EMPLOYMENT_GROUP",
    y="customers",
    text="customers",
    title="Customers by Employment Duration"
)

fig_distribution.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_distribution.update_xaxes(
    title="Employment Duration"
)

fig_distribution.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY EMPLOYMENT
# ============================================================

st.subheader("⚠️ Default Rate by Employment Duration")

employment_risk = default_rate_by_employment_group(df)

fig_employment_risk = px.bar(
    employment_risk,
    x="EMPLOYMENT_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Employment Duration"
)

fig_employment_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_employment_risk.update_xaxes(
    title="Employment Duration"
)

fig_employment_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_employment_risk,
    use_container_width=True
)


# ============================================================
# FINANCIAL PROFILE
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Employment Duration")

financial_data = employment_financial_summary(df)

financial_long = financial_data.melt(
    id_vars="EMPLOYMENT_GROUP",
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
    x="EMPLOYMENT_GROUP",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Employment"
)

fig_financial.update_xaxes(
    title="Employment Duration"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# OCCUPATION RISK
# ============================================================

st.divider()

st.subheader("👷 Default Rate by Occupation")

occupation_data = occupation_risk_summary(df)

min_occupation_customers = st.slider(
    "Minimum customers per occupation",
    min_value=10,
    max_value=200,
    value=50,
    step=10
)

occupation_filtered = occupation_data[
    occupation_data["customers"] >= min_occupation_customers
].sort_values(
    "default_rate",
    ascending=False
)

fig_occupation = px.bar(
    occupation_filtered.head(15),
    x="default_rate",
    y="OCCUPATION_TYPE",
    orientation="h",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Top Occupations by Observed Default Rate"
)

fig_occupation.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_occupation.update_xaxes(
    title="Default Rate (%)"
)

fig_occupation.update_yaxes(
    title="Occupation"
)

st.plotly_chart(
    fig_occupation,
    use_container_width=True
)


# ============================================================
# ORGANIZATION RISK
# ============================================================

st.subheader("🏢 Default Rate by Organization Type")

min_org_customers = st.slider(
    "Minimum customers per organization",
    min_value=5,
    max_value=200,
    value=30,
    step=5
)

organization_data = organization_risk_summary(df)

organization_filtered = organization_data[
    organization_data["customers"] >= min_org_customers
].sort_values(
    "default_rate",
    ascending=False
)

fig_organization = px.bar(
    organization_filtered.head(15),
    x="default_rate",
    y="ORGANIZATION_TYPE",
    orientation="h",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Top Organization Types by Observed Default Rate"
)

fig_organization.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_organization.update_xaxes(
    title="Default Rate (%)"
)

fig_organization.update_yaxes(
    title="Organization Type"
)

st.plotly_chart(
    fig_organization,
    use_container_width=True
)


# ============================================================
# RISK TABLE
# ============================================================

st.divider()

st.subheader("📋 Employment Risk Summary")

display_risk = employment_risk.copy()

display_risk["default_rate"] = (
    display_risk["default_rate"].round(2)
)

st.dataframe(
    display_risk,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.subheader("💡 Employment Insights")

highest_employment_risk = employment_risk.loc[
    employment_risk["default_rate"].idxmax()
]

lowest_employment_risk = employment_risk.loc[
    employment_risk["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Observed Employment Risk**

        {highest_employment_risk['EMPLOYMENT_GROUP']}

        Default Rate:
        **{highest_employment_risk['default_rate']:.2f}%**

        Customers:
        **{highest_employment_risk['customers']:,}**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Observed Employment Risk**

        {lowest_employment_risk['EMPLOYMENT_GROUP']}

        Default Rate:
        **{lowest_employment_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_employment_risk['customers']:,}**
        """
    )


st.caption(
    "Employment duration excludes the Home Credit special value "
    "365243, which represents unavailable employment information. "
    "Default rates describe observed patterns and should not be "
    "interpreted as causal relationships."
)