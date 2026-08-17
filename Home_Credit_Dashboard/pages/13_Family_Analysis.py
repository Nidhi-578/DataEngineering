import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    family_status_summary,
    children_distribution,
    family_size_distribution,
    default_rate_by_family_size,
    family_financial_summary,
    children_risk_summary,
)


st.set_page_config(
    page_title="Family Analysis",
    page_icon="👨‍👩‍👧",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading family analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("👨‍👩‍👧 Family & Household Analysis")

st.markdown(
    """
    Analyze family status, number of children, household size,
    financial characteristics, and observed default risk.
    """
)


# ============================================================
# FAMILY STATUS
# ============================================================

family_status = family_status_summary(df)

total_customers = family_status["customers"].sum()

most_common_status = (
    family_status
    .sort_values("customers", ascending=False)
    .iloc[0]
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Most Common Family Status",
        most_common_status["NAME_FAMILY_STATUS"]
    )

with col3:
    st.metric(
        "Customers in Largest Group",
        f"{most_common_status['customers']:,}"
    )


st.divider()

st.subheader("💍 Family Status Distribution")

fig_family = px.bar(
    family_status,
    x="NAME_FAMILY_STATUS",
    y="customers",
    text="customers",
    title="Customers by Family Status"
)

fig_family.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_family.update_xaxes(
    title="Family Status"
)

fig_family.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_family,
    use_container_width=True
)


# ============================================================
# FAMILY STATUS DEFAULT RATE
# ============================================================

st.subheader("⚠️ Default Rate by Family Status")

fig_family_risk = px.bar(
    family_status,
    x="NAME_FAMILY_STATUS",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Family Status"
)

fig_family_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_family_risk.update_xaxes(
    title="Family Status"
)

fig_family_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_family_risk,
    use_container_width=True
)


# ============================================================
# CHILDREN DISTRIBUTION
# ============================================================

st.divider()

st.subheader("👶 Number of Children")

children_data = children_distribution(df)

fig_children = px.bar(
    children_data,
    x="CNT_CHILDREN",
    y="customers",
    text="customers",
    title="Customers by Number of Children"
)

fig_children.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_children.update_xaxes(
    title="Number of Children"
)

fig_children.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_children,
    use_container_width=True
)


# ============================================================
# CHILDREN DEFAULT RISK
# ============================================================

st.subheader("⚠️ Default Rate by Number of Children")

children_risk = children_risk_summary(df)

minimum_children_customers = st.slider(
    "Minimum customers per children group",
    min_value=5,
    max_value=200,
    value=50,
    step=5
)

children_risk_filtered = children_risk[
    children_risk["customers"] >= minimum_children_customers
]

fig_children_risk = px.bar(
    children_risk_filtered,
    x="CNT_CHILDREN",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Number of Children"
)

fig_children_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_children_risk.update_xaxes(
    title="Number of Children"
)

fig_children_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_children_risk,
    use_container_width=True
)


# ============================================================
# FAMILY SIZE
# ============================================================

st.divider()

st.subheader("🏠 Household Size")

family_size = family_size_distribution(df)

fig_family_size = px.bar(
    family_size,
    x="CNT_FAM_MEMBERS",
    y="customers",
    text="customers",
    title="Customers by Family Size"
)

fig_family_size.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_family_size.update_xaxes(
    title="Family Members"
)

fig_family_size.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_family_size,
    use_container_width=True
)


# ============================================================
# FAMILY SIZE DEFAULT RISK
# ============================================================

st.subheader("⚠️ Default Rate by Family Size")

family_size_risk = default_rate_by_family_size(df)

minimum_family_customers = st.slider(
    "Minimum customers per family-size group",
    min_value=5,
    max_value=200,
    value=50,
    step=5
)

family_size_filtered = family_size_risk[
    family_size_risk["customers"] >= minimum_family_customers
]

fig_family_size_risk = px.bar(
    family_size_filtered,
    x="CNT_FAM_MEMBERS",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Family Size"
)

fig_family_size_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_family_size_risk.update_xaxes(
    title="Family Members"
)

fig_family_size_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_family_size_risk,
    use_container_width=True
)


# ============================================================
# FINANCIAL PROFILE
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Family Status")

financial_data = family_financial_summary(df)

financial_long = financial_data.melt(
    id_vars="NAME_FAMILY_STATUS",
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
    x="NAME_FAMILY_STATUS",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Family Status"
)

fig_financial.update_xaxes(
    title="Family Status"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# FAMILY RISK TABLE
# ============================================================

st.divider()

st.subheader("📋 Family Risk Summary")

display_family = family_status.copy()

display_family["default_rate"] = (
    display_family["default_rate"].round(2)
)

st.dataframe(
    display_family,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.subheader("💡 Family & Household Insights")

meaningful_family = family_status[
    family_status["customers"] >= 50
]

highest_family_risk = meaningful_family.loc[
    meaningful_family["default_rate"].idxmax()
]

lowest_family_risk = meaningful_family.loc[
    meaningful_family["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Observed Family-Status Risk**

        {highest_family_risk['NAME_FAMILY_STATUS']}

        Default Rate:
        **{highest_family_risk['default_rate']:.2f}%**

        Customers:
        **{highest_family_risk['customers']:,}**
        """
    )

with col2:
    st.success(
        f"""
        **Lowest Observed Family-Status Risk**

        {lowest_family_risk['NAME_FAMILY_STATUS']}

        Default Rate:
        **{lowest_family_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_family_risk['customers']:,}**
        """
    )


st.caption(
    "Default rates describe observed patterns in the dataset. "
    "Small family-size groups should be interpreted cautiously."
)