import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    target_summary,
    default_rate_by_gender,
    default_rate_by_income_type,
    default_rate_by_education,
    default_rate_by_contract,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Default Analysis",
    page_icon="🎯",
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


with st.spinner("Loading default analysis data..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🎯 Default / Target Analysis")

st.markdown(
    """
    Analyze customer payment difficulty and default patterns
    across key customer segments.
    """
)


# ============================================================
# TARGET SUMMARY
# ============================================================

summary = target_summary(df)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Customers",
        f"{summary['total_customers']:,}"
    )


with col2:

    st.metric(
        "Default Customers",
        f"{summary['default_customers']:,}"
    )


with col3:

    st.metric(
        "Non-Default Customers",
        f"{summary['non_default_customers']:,}"
    )


with col4:

    st.metric(
        "Default Rate",
        f"{summary['default_rate']:.2f}%"
    )


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Default vs Non-Default")


target_data = pd.DataFrame(
    {
        "Status": [
            "Non-Default",
            "Default"
        ],
        "Customers": [
            summary["non_default_customers"],
            summary["default_customers"]
        ]
    }
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# BAR CHART
# ------------------------------------------------------------

with col1:

    fig_bar = px.bar(
        target_data,
        x="Status",
        y="Customers",
        text="Customers",
        title="Customer Count by Default Status"
    )

    fig_bar.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig_bar.update_yaxes(
        title="Customers"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


# ------------------------------------------------------------
# DONUT CHART
# ------------------------------------------------------------

with col2:

    fig_donut = px.pie(
        target_data,
        names="Status",
        values="Customers",
        hole=0.55,
        title="Default vs Non-Default Distribution"
    )

    fig_donut.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )


# ============================================================
# DEFAULT RATE BY GENDER
# ============================================================

st.divider()

st.subheader("👥 Default Rate by Gender")


gender_data = default_rate_by_gender(df)


fig_gender = px.bar(
    gender_data,
    x="CODE_GENDER",
    y="default_rate",
    text="default_rate",
    title="Default Rate by Gender"
)


fig_gender.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_gender.update_yaxes(
    title="Default Rate (%)"
)


fig_gender.update_xaxes(
    title="Gender"
)


st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY INCOME TYPE
# ============================================================

st.subheader("💼 Default Rate by Income Type")


income_data = default_rate_by_income_type(df)


fig_income = px.bar(
    income_data,
    x="default_rate",
    y="NAME_INCOME_TYPE",
    orientation="h",
    text="default_rate",
    title="Default Rate by Income Type"
)


fig_income.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_income.update_xaxes(
    title="Default Rate (%)"
)


fig_income.update_yaxes(
    title="Income Type"
)


st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY EDUCATION
# ============================================================

st.subheader("🎓 Default Rate by Education")


education_data = default_rate_by_education(df)


fig_education = px.bar(
    education_data,
    x="default_rate",
    y="NAME_EDUCATION_TYPE",
    orientation="h",
    text="default_rate",
    title="Default Rate by Education Level"
)


fig_education.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_education.update_xaxes(
    title="Default Rate (%)"
)


fig_education.update_yaxes(
    title="Education"
)


st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY CONTRACT TYPE
# ============================================================

st.subheader("📄 Default Rate by Contract Type")


contract_data = default_rate_by_contract(df)


fig_contract = px.bar(
    contract_data,
    x="NAME_CONTRACT_TYPE",
    y="default_rate",
    text="default_rate",
    title="Default Rate by Contract Type"
)


fig_contract.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_contract.update_yaxes(
    title="Default Rate (%)"
)


fig_contract.update_xaxes(
    title="Contract Type"
)


st.plotly_chart(
    fig_contract,
    use_container_width=True
)


# ============================================================
# KEY INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Default Insights")


highest_gender = gender_data.loc[
    gender_data["default_rate"].idxmax()
]

highest_income = income_data.loc[
    income_data["default_rate"].idxmax()
]

highest_education = education_data.loc[
    education_data["default_rate"].idxmax()
]

highest_contract = contract_data.loc[
    contract_data["default_rate"].idxmax()
]


col1, col2 = st.columns(2)


with col1:

    st.info(
        f"""
        **Highest Gender Risk**

        {highest_gender['CODE_GENDER']}

        Default Rate:
        **{highest_gender['default_rate']:.2f}%**
        """
    )


with col2:

    st.info(
        f"""
        **Highest Income-Type Risk**

        {highest_income['NAME_INCOME_TYPE']}

        Default Rate:
        **{highest_income['default_rate']:.2f}%**
        """
    )


col1, col2 = st.columns(2)


with col1:

    st.info(
        f"""
        **Highest Education Risk**

        {highest_education['NAME_EDUCATION_TYPE']}

        Default Rate:
        **{highest_education['default_rate']:.2f}%**
        """
    )


with col2:

    st.info(
        f"""
        **Highest Contract Risk**

        {highest_contract['NAME_CONTRACT_TYPE']}

        Default Rate:
        **{highest_contract['default_rate']:.2f}%**
        """
    )