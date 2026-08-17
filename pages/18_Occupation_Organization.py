import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    occupation_risk_summary,
    organization_risk_summary,
    occupation_financial_summary,
    organization_financial_summary,
    occupation_income_risk,
    organization_income_risk,
)


st.set_page_config(
    page_title="Occupation & Organization",
    page_icon="💼",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading occupation and organization analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("💼 Occupation & Organization Risk Analysis")

st.markdown(
    """
    Analyze observed default risk and financial characteristics
    across occupations and organization types.
    """
)


# ============================================================
# ANALYSIS DATA
# ============================================================

occupation_data = occupation_risk_summary(df)
organization_data = organization_risk_summary(df)

occupation_financial = occupation_financial_summary(df)
organization_financial = organization_financial_summary(df)

occupation_income = occupation_income_risk(df)
organization_income = organization_income_risk(df)


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Occupation Categories",
        f"{len(occupation_data):,}"
    )

with col2:
    st.metric(
        "Organization Categories",
        f"{len(organization_data):,}"
    )

with col3:
    st.metric(
        "Occupation Records",
        f"{occupation_data['customers'].sum():,}"
    )

with col4:
    st.metric(
        "Organization Records",
        f"{organization_data['customers'].sum():,}"
    )


# ============================================================
# OCCUPATION DEFAULT RISK
# ============================================================

st.divider()

st.subheader("👷 Default Rate by Occupation")

minimum_occupation_customers = st.slider(
    "Minimum customers for occupation risk chart",
    min_value=10,
    max_value=500,
    value=50,
    step=10
)

occupation_filtered = occupation_data[
    occupation_data["customers"] >= minimum_occupation_customers
].sort_values(
    "default_rate",
    ascending=True
)

fig_occupation_risk = px.bar(
    occupation_filtered,
    x="default_rate",
    y="OCCUPATION_TYPE",
    orientation="h",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Observed Default Rate by Occupation"
)

fig_occupation_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_occupation_risk.update_xaxes(
    title="Default Rate (%)"
)

fig_occupation_risk.update_yaxes(
    title="Occupation"
)

st.plotly_chart(
    fig_occupation_risk,
    use_container_width=True
)


# ============================================================
# OCCUPATION CUSTOMER DISTRIBUTION
# ============================================================

st.subheader("👥 Customers by Occupation")

occupation_volume = occupation_data.sort_values(
    "customers",
    ascending=False
)

fig_occupation_volume = px.bar(
    occupation_volume,
    x="OCCUPATION_TYPE",
    y="customers",
    text="customers",
    title="Customer Distribution by Occupation"
)

fig_occupation_volume.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_occupation_volume.update_xaxes(
    title="Occupation",
    tickangle=-35
)

fig_occupation_volume.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_occupation_volume,
    use_container_width=True
)


# ============================================================
# ORGANIZATION RISK
# ============================================================

st.divider()

st.subheader("🏢 Default Rate by Organization Type")

minimum_organization_customers = st.slider(
    "Minimum customers for organization risk chart",
    min_value=10,
    max_value=500,
    value=50,
    step=10
)

organization_filtered = organization_data[
    organization_data["customers"] >= minimum_organization_customers
].sort_values(
    "default_rate",
    ascending=True
)

fig_organization_risk = px.bar(
    organization_filtered,
    x="default_rate",
    y="ORGANIZATION_TYPE",
    orientation="h",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Observed Default Rate by Organization Type"
)

fig_organization_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_organization_risk.update_xaxes(
    title="Default Rate (%)"
)

fig_organization_risk.update_yaxes(
    title="Organization Type"
)

st.plotly_chart(
    fig_organization_risk,
    use_container_width=True
)


# ============================================================
# ORGANIZATION VOLUME
# ============================================================

st.subheader("🏢 Customer Distribution by Organization")

organization_volume = organization_data.sort_values(
    "customers",
    ascending=False
).head(20)

fig_organization_volume = px.bar(
    organization_volume,
    x="ORGANIZATION_TYPE",
    y="customers",
    text="customers",
    title="Top 20 Organizations by Customer Count"
)

fig_organization_volume.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_organization_volume.update_xaxes(
    title="Organization",
    tickangle=-45
)

fig_organization_volume.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_organization_volume,
    use_container_width=True
)


# ============================================================
# OCCUPATION FINANCIAL PROFILE
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Occupation")

occupation_financial_long = occupation_financial.melt(
    id_vars="OCCUPATION_TYPE",
    value_vars=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY"
    ],
    var_name="metric",
    value_name="average_value"
)

occupation_financial_long["metric"] = (
    occupation_financial_long["metric"].map(
        {
            "AMT_INCOME_TOTAL": "Income",
            "AMT_CREDIT": "Credit",
            "AMT_ANNUITY": "Annuity"
        }
    )
)

fig_occupation_financial = px.bar(
    occupation_financial_long,
    x="OCCUPATION_TYPE",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Financial Metrics by Occupation"
)

fig_occupation_financial.update_xaxes(
    title="Occupation",
    tickangle=-35
)

fig_occupation_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_occupation_financial,
    use_container_width=True
)


# ============================================================
# ORGANIZATION FINANCIAL PROFILE
# ============================================================

st.subheader("💰 Financial Profile by Organization")

organization_financial_long = organization_financial.melt(
    id_vars="ORGANIZATION_TYPE",
    value_vars=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY"
    ],
    var_name="metric",
    value_name="average_value"
)

organization_financial_long["metric"] = (
    organization_financial_long["metric"].map(
        {
            "AMT_INCOME_TOTAL": "Income",
            "AMT_CREDIT": "Credit",
            "AMT_ANNUITY": "Annuity"
        }
    )
)

fig_organization_financial = px.bar(
    organization_financial_long,
    x="ORGANIZATION_TYPE",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Financial Metrics by Organization"
)

fig_organization_financial.update_xaxes(
    title="Organization",
    tickangle=-45
)

fig_organization_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_organization_financial,
    use_container_width=True
)


# ============================================================
# OCCUPATION × INCOME RISK
# ============================================================

st.divider()

st.subheader("🔎 Occupation × Income Risk")

minimum_occ_income_customers = st.slider(
    "Minimum customers for occupation × income",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

occupation_income_filtered = occupation_income[
    occupation_income["customers"] >= minimum_occ_income_customers
]

fig_occ_income = px.density_heatmap(
    occupation_income_filtered,
    x="INCOME_GROUP",
    y="OCCUPATION_TYPE",
    z="default_rate",
    text_auto=".2f",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Occupation and Income Group"
)

fig_occ_income.update_xaxes(
    title="Income Group"
)

fig_occ_income.update_yaxes(
    title="Occupation"
)

st.plotly_chart(
    fig_occ_income,
    use_container_width=True
)


# ============================================================
# ORGANIZATION × INCOME RISK
# ============================================================

st.subheader("🔎 Organization × Income Risk")

minimum_org_income_customers = st.slider(
    "Minimum customers for organization × income",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

organization_income_filtered = organization_income[
    organization_income["customers"] >= minimum_org_income_customers
]

fig_org_income = px.density_heatmap(
    organization_income_filtered,
    x="INCOME_GROUP",
    y="ORGANIZATION_TYPE",
    z="default_rate",
    text_auto=".2f",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Organization and Income Group"
)

fig_org_income.update_xaxes(
    title="Income Group"
)

fig_org_income.update_yaxes(
    title="Organization Type"
)

st.plotly_chart(
    fig_org_income,
    use_container_width=True
)


# ============================================================
# TOP RISK OCCUPATIONS
# ============================================================

st.divider()

st.subheader("🏆 Highest Observed Occupation Risk")

top_occupations = (
    occupation_data[
        occupation_data["customers"] >= minimum_occupation_customers
    ]
    .sort_values(
        "default_rate",
        ascending=False
    )
    .head(10)
    .copy()
)

top_occupations["default_rate"] = (
    top_occupations["default_rate"].round(2)
)

st.dataframe(
    top_occupations,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# TOP RISK ORGANIZATIONS
# ============================================================

st.subheader("🏆 Highest Observed Organization Risk")

top_organizations = (
    organization_data[
        organization_data["customers"] >= minimum_organization_customers
    ]
    .sort_values(
        "default_rate",
        ascending=False
    )
    .head(10)
    .copy()
)

top_organizations["default_rate"] = (
    top_organizations["default_rate"].round(2)
)

st.dataframe(
    top_organizations,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Occupation & Organization Insights")

if not occupation_filtered.empty:

    highest_occupation = occupation_filtered.loc[
        occupation_filtered["default_rate"].idxmax()
    ]

else:

    highest_occupation = occupation_data.loc[
        occupation_data["default_rate"].idxmax()
    ]


if not organization_filtered.empty:

    highest_organization = organization_filtered.loc[
        organization_filtered["default_rate"].idxmax()
    ]

else:

    highest_organization = organization_data.loc[
        organization_data["default_rate"].idxmax()
    ]


col1, col2 = st.columns(2)

with col1:

    st.warning(
        f"""
        **Highest Observed Occupation Risk**

        Occupation:
        **{highest_occupation['OCCUPATION_TYPE']}**

        Default Rate:
        **{highest_occupation['default_rate']:.2f}%**

        Customers:
        **{highest_occupation['customers']:,}**
        """
    )


with col2:

    st.warning(
        f"""
        **Highest Observed Organization Risk**

        Organization:
        **{highest_organization['ORGANIZATION_TYPE']}**

        Default Rate:
        **{highest_organization['default_rate']:.2f}%**

        Customers:
        **{highest_organization['customers']:,}**
        """
    )


st.caption(
    "Default rates describe observed patterns in the dataset. "
    "Small occupation or organization segments should be "
    "interpreted cautiously. These relationships should not "
    "be treated as causal."
)