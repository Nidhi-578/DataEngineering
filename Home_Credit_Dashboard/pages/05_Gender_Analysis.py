import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    gender_summary,
    gender_default_summary,
    gender_financial_summary,
    gender_education_risk,
    gender_income_risk,
)


st.set_page_config(
    page_title="Gender Analysis",
    page_icon="⚥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading gender analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("⚥ Gender Analysis")

st.markdown(
    """
    Analyze customer distribution, financial characteristics,
    and default risk across gender segments.
    """
)


# ============================================================
# SUMMARY
# ============================================================

gender_data = gender_summary(df)

default_data = gender_default_summary(df)

financial_data = gender_financial_summary(df)


# ============================================================
# KPI CARDS
# ============================================================

total_customers = len(df)

female_count = (
    df["CODE_GENDER"] == "F"
).sum()

male_count = (
    df["CODE_GENDER"] == "M"
).sum()

overall_default_rate = (
    df["TARGET"].mean() * 100
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )


with col2:
    st.metric(
        "Female Customers",
        f"{female_count:,}"
    )


with col3:
    st.metric(
        "Male Customers",
        f"{male_count:,}"
    )


with col4:
    st.metric(
        "Overall Default Rate",
        f"{overall_default_rate:.2f}%"
    )


# ============================================================
# CUSTOMER DISTRIBUTION
# ============================================================

st.divider()

st.subheader("👥 Gender Distribution")

col1, col2 = st.columns(2)


with col1:

    fig_distribution = px.bar(
        gender_data,
        x="gender",
        y="customers",
        text="customers",
        title="Customers by Gender"
    )

    fig_distribution.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig_distribution.update_xaxes(
        title="Gender"
    )

    fig_distribution.update_yaxes(
        title="Customers"
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True
    )


with col2:

    fig_percentage = px.pie(
        gender_data,
        names="gender",
        values="customers",
        hole=0.5,
        title="Gender Percentage Distribution"
    )

    fig_percentage.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_percentage,
        use_container_width=True
    )


# ============================================================
# DEFAULT RISK
# ============================================================

st.divider()

st.subheader("⚠️ Default Risk by Gender")


col1, col2 = st.columns(2)


with col1:

    fig_default_rate = px.bar(
        default_data,
        x="CODE_GENDER",
        y="default_rate",
        text="default_rate",
        title="Default Rate by Gender"
    )

    fig_default_rate.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_default_rate.update_yaxes(
        title="Default Rate (%)"
    )

    fig_default_rate.update_xaxes(
        title="Gender"
    )

    st.plotly_chart(
        fig_default_rate,
        use_container_width=True
    )


with col2:

    default_count_data = default_data[
        [
            "CODE_GENDER",
            "defaults",
            "non_defaults"
        ]
    ].melt(
        id_vars="CODE_GENDER",
        var_name="status",
        value_name="customers"
    )

    default_count_data["status"] = (
        default_count_data["status"]
        .map(
            {
                "defaults": "Default",
                "non_defaults": "Non-Default"
            }
        )
    )

    fig_default_count = px.bar(
        default_count_data,
        x="CODE_GENDER",
        y="customers",
        color="status",
        barmode="group",
        text="customers",
        title="Default vs Non-Default Customers"
    )

    fig_default_count.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig_default_count.update_yaxes(
        title="Customers"
    )

    st.plotly_chart(
        fig_default_count,
        use_container_width=True
    )


# ============================================================
# FINANCIAL CHARACTERISTICS
# ============================================================

st.divider()

st.subheader("💰 Financial Characteristics by Gender")


financial_long = financial_data.melt(
    id_vars="CODE_GENDER",
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
    x="CODE_GENDER",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Gender"
)

fig_financial.update_xaxes(
    title="Gender"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# GENDER × EDUCATION
# ============================================================

st.subheader("🎓 Gender × Education Risk")


education_risk = gender_education_risk(df)


fig_education = px.bar(
    education_risk,
    x="NAME_EDUCATION_TYPE",
    y="default_rate",
    color="CODE_GENDER",
    barmode="group",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Gender and Education"
)


fig_education.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_education.update_xaxes(
    title="Education",
    tickangle=-30
)


fig_education.update_yaxes(
    title="Default Rate (%)"
)


st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ============================================================
# GENDER × INCOME TYPE
# ============================================================

st.subheader("💼 Gender × Income Type Risk")


income_risk = gender_income_risk(df)


fig_income = px.bar(
    income_risk,
    x="NAME_INCOME_TYPE",
    y="default_rate",
    color="CODE_GENDER",
    barmode="group",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Gender and Income Type"
)


fig_income.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_income.update_xaxes(
    title="Income Type",
    tickangle=-30
)


fig_income.update_yaxes(
    title="Default Rate (%)"
)


st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ============================================================
# KEY INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Gender Risk Insights")


highest_gender = default_data.loc[
    default_data["default_rate"].idxmax()
]


income_risk_filtered = income_risk[
    income_risk["customers"] >= 50
]


if not income_risk_filtered.empty:

    highest_income_segment = (
        income_risk_filtered.loc[
            income_risk_filtered["default_rate"].idxmax()
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.warning(
            f"""
            **Highest Gender Default Rate**

            Gender: **{highest_gender['CODE_GENDER']}**

            Default Rate:
            **{highest_gender['default_rate']:.2f}%**

            Customers:
            **{highest_gender['customers']:,}**
            """
        )

    with col2:

        st.info(
            f"""
            **Highest Meaningful Gender × Income Segment**

            Gender: **{highest_income_segment['CODE_GENDER']}**

            Income Type:
            **{highest_income_segment['NAME_INCOME_TYPE']}**

            Default Rate:
            **{highest_income_segment['default_rate']:.2f}%**

            Customers:
            **{highest_income_segment['customers']:,}**
            """
        )


st.caption(
    "Risk rates describe observed patterns in the dataset. "
    "Very small segments should not be interpreted as reliable "
    "risk estimates."
)