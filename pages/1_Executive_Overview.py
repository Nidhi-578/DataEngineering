import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    calculate_kpis,
    default_summary,
    applications_by_category,
    credit_statistics,
    executive_insights,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Executive Overview",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/application_train.csv"
    )


with st.spinner("Loading Home Credit dataset..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🏦 Home Credit Risk Dashboard")

st.markdown(
    """
    ## Executive Overview

    Management-level overview of loan applications,
    customer characteristics, and credit default risk.
    """
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# Gender
gender_options = ["All"] + sorted(
    df["CODE_GENDER"]
    .dropna()
    .unique()
    .tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)


# Contract Type
contract_options = ["All"] + sorted(
    df["NAME_CONTRACT_TYPE"]
    .dropna()
    .unique()
    .tolist()
)

selected_contract = st.sidebar.selectbox(
    "Contract Type",
    contract_options
)


# Income Type
income_options = ["All"] + sorted(
    df["NAME_INCOME_TYPE"]
    .dropna()
    .unique()
    .tolist()
)

selected_income = st.sidebar.selectbox(
    "Income Type",
    income_options
)


# Education
education_options = ["All"] + sorted(
    df["NAME_EDUCATION_TYPE"]
    .dropna()
    .unique()
    .tolist()
)

selected_education = st.sidebar.selectbox(
    "Education",
    education_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["CODE_GENDER"] == selected_gender
    ]


if selected_contract != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_CONTRACT_TYPE"] == selected_contract
    ]


if selected_income != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_INCOME_TYPE"] == selected_income
    ]


if selected_education != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_EDUCATION_TYPE"] == selected_education
    ]


# ============================================================
# CALCULATE METRICS
# ============================================================

kpis = calculate_kpis(filtered_df)

credit_stats = credit_statistics(filtered_df)

insights = executive_insights(filtered_df)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Portfolio KPIs")


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Applications",
        f"{kpis['total_applications']:,}"
    )


with col2:

    st.metric(
        "Default Customers",
        f"{kpis['total_defaults']:,}"
    )


with col3:

    non_defaults = (
        kpis["total_applications"]
        - kpis["total_defaults"]
    )

    st.metric(
        "Non-Default Customers",
        f"{non_defaults:,}"
    )


with col4:

    st.metric(
        "Default Rate",
        f"{kpis['default_rate']:.2f}%"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:

    st.metric(
        "Total Credit Amount",
        f"₹{credit_stats['total_credit']:,.0f}"
    )


with col6:

    st.metric(
        "Average Credit Amount",
        f"₹{credit_stats['average_credit']:,.0f}"
    )


with col7:

    st.metric(
        "Average Income",
        f"₹{kpis['average_income']:,.0f}"
    )


with col8:

    st.metric(
        "Average Annuity",
        f"₹{kpis['average_annuity']:,.0f}"
    )


# ============================================================
# DEFAULT DISTRIBUTION
# ============================================================

st.divider()

st.subheader("🎯 Default vs Non-Default")


default_data = default_summary(filtered_df)


fig_default = px.pie(
    default_data,
    names="status",
    values="customers",
    hole=0.45,
    title="Customer Default Distribution"
)

fig_default.update_layout(
    legend_title="Customer Status"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ============================================================
# APPLICATIONS BY GENDER
# ============================================================

st.subheader("👥 Applications by Gender")


gender_data = applications_by_category(
    filtered_df,
    "CODE_GENDER"
)


fig_gender = px.bar(
    gender_data,
    x="category",
    y="applications",
    title="Applications by Gender",
    text="applications"
)

fig_gender.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ============================================================
# APPLICATIONS BY CONTRACT TYPE
# ============================================================

st.subheader("📄 Applications by Contract Type")


contract_data = applications_by_category(
    filtered_df,
    "NAME_CONTRACT_TYPE"
)


fig_contract = px.bar(
    contract_data,
    x="category",
    y="applications",
    title="Applications by Contract Type",
    text="applications"
)

fig_contract.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_contract,
    use_container_width=True
)


# ============================================================
# APPLICATIONS BY INCOME TYPE
# ============================================================

st.subheader("💼 Applications by Income Type")


income_data = applications_by_category(
    filtered_df,
    "NAME_INCOME_TYPE"
)


income_data = income_data.sort_values(
    "applications",
    ascending=True
)


fig_income = px.bar(
    income_data,
    x="applications",
    y="category",
    orientation="h",
    title="Applications by Income Type",
    text="applications"
)

fig_income.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ============================================================
# CREDIT AMOUNT DISTRIBUTION
# ============================================================

st.subheader("💰 Credit Amount Distribution")


fig_credit = px.histogram(
    filtered_df,
    x="AMT_CREDIT",
    nbins=50,
    title="Distribution of Credit Amount",
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Business Insights")


col1, col2 = st.columns(2)


with col1:

    st.info(
        f"""
        **Overall Default Rate**

        {insights['default_rate']:.2f}%
        """
    )

    st.info(
        f"""
        **Average Customer Income**

        ₹{insights['average_income']:,.0f}
        """
    )

    st.info(
        f"""
        **Average Loan Amount**

        ₹{insights['average_credit']:,.0f}
        """
    )


with col2:

    st.info(
        f"""
        **Most Common Income Type**

        {insights['most_common_income']}
        """
    )

    st.info(
        f"""
        **Most Common Education Level**

        {insights['most_common_education']}
        """
    )

    st.warning(
        f"""
        **Highest Risk Customer Segment**

        {insights['highest_risk_segment']}
        """
    )