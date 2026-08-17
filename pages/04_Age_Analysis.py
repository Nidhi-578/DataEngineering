import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    prepare_customer_data,
    age_distribution,
    default_rate_by_age,
    age_financial_summary,
)


st.set_page_config(
    page_title="Age Analysis",
    page_icon="🎂",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading age analysis..."):
    df = load_data()


# ============================================================
# PREPARE DATA
# ============================================================

df = prepare_customer_data(df)


# ============================================================
# HEADER
# ============================================================

st.title("🎂 Age Analysis")

st.markdown(
    """
    Analyze applicant age distribution, age segments,
    financial characteristics, and default risk.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔎 Age Filters")

age_groups = [
    "All",
    "18-25",
    "26-35",
    "36-45",
    "46-55",
    "56-65",
    "65+",
]

selected_age_group = st.sidebar.selectbox(
    "Age Group",
    age_groups
)


filtered_df = df.copy()

if selected_age_group != "All":
    filtered_df = filtered_df[
        filtered_df["AGE_GROUP"].astype(str)
        == selected_age_group
    ]


# ============================================================
# KPIs
# ============================================================

total_customers = len(filtered_df)

average_age = filtered_df["AGE"].mean()

minimum_age = filtered_df["AGE"].min()

maximum_age = filtered_df["AGE"].max()

default_rate = filtered_df["TARGET"].mean() * 100


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Average Age",
        f"{average_age:.1f} years"
    )

with col3:
    st.metric(
        "Age Range",
        f"{minimum_age:.0f}–{maximum_age:.0f}"
    )

with col4:
    st.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )


# ============================================================
# AGE DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Customer Age Distribution")

age_data = age_distribution(
    filtered_df
)


fig_age_distribution = px.bar(
    age_data,
    x="AGE_GROUP",
    y="customers",
    text="customers",
    title="Customers by Age Group"
)

fig_age_distribution.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_age_distribution.update_xaxes(
    title="Age Group"
)

fig_age_distribution.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_age_distribution,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY AGE
# ============================================================

st.subheader("⚠️ Default Rate by Age Group")

age_risk = default_rate_by_age(
    filtered_df
)


fig_age_risk = px.bar(
    age_risk,
    x="AGE_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Age Group"
)

fig_age_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_age_risk.update_xaxes(
    title="Age Group"
)

fig_age_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_age_risk,
    use_container_width=True
)


# ============================================================
# FINANCIAL CHARACTERISTICS BY AGE
# ============================================================

st.divider()

st.subheader("💰 Financial Characteristics by Age")

financial_data = age_financial_summary(
    filtered_df
)


financial_long = financial_data.melt(
    id_vars="AGE_GROUP",
    value_vars=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY"
    ],
    var_name="metric",
    value_name="average_value"
)


financial_long["metric"] = financial_long[
    "metric"
].map(
    {
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit",
        "AMT_ANNUITY": "Annuity"
    }
)


fig_financial = px.bar(
    financial_long,
    x="AGE_GROUP",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Age Group"
)

fig_financial.update_xaxes(
    title="Age Group"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# AGE VS CREDIT
# ============================================================

st.subheader("📈 Age vs Credit Amount")

scatter_df = filtered_df[
    [
        "AGE",
        "AMT_CREDIT",
        "TARGET",
        "AMT_INCOME_TOTAL"
    ]
].dropna()


# Limit points for browser performance
if len(scatter_df) > 10000:
    scatter_df = scatter_df.sample(
        10000,
        random_state=42
    )


scatter_df["Status"] = scatter_df[
    "TARGET"
].map(
    {
        0: "Non-Default",
        1: "Default"
    }
)


fig_scatter = px.scatter(
    scatter_df,
    x="AGE",
    y="AMT_CREDIT",
    color="Status",
    hover_data=[
        "AMT_INCOME_TOTAL"
    ],
    opacity=0.6,
    title="Age vs Credit Amount"
)

fig_scatter.update_xaxes(
    title="Age (Years)"
)

fig_scatter.update_yaxes(
    title="Credit Amount"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ============================================================
# AGE VS INCOME
# ============================================================

st.subheader("💵 Age vs Income")

fig_income_age = px.scatter(
    scatter_df,
    x="AGE",
    y="AMT_INCOME_TOTAL",
    color="Status",
    opacity=0.6,
    title="Age vs Income"
)

fig_income_age.update_xaxes(
    title="Age (Years)"
)

fig_income_age.update_yaxes(
    title="Income"
)

st.plotly_chart(
    fig_income_age,
    use_container_width=True
)


# ============================================================
# KEY INSIGHT
# ============================================================

st.divider()

st.subheader("💡 Age Risk Insight")

if not age_risk.empty:

    highest_risk = age_risk.loc[
        age_risk["default_rate"].idxmax()
    ]

    lowest_risk = age_risk.loc[
        age_risk["default_rate"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.warning(
            f"""
            **Highest observed default rate**

            Age Group: **{highest_risk['AGE_GROUP']}**

            Default Rate:
            **{highest_risk['default_rate']:.2f}%**

            Customers:
            **{highest_risk['customers']:,}**
            """
        )

    with col2:
        st.success(
            f"""
            **Lowest observed default rate**

            Age Group: **{lowest_risk['AGE_GROUP']}**

            Default Rate:
            **{lowest_risk['default_rate']:.2f}%**

            Customers:
            **{lowest_risk['customers']:,}**
            """
        )

st.caption(
    "Default rates describe observed patterns in the dataset "
    "and should not be interpreted as causal relationships."
)