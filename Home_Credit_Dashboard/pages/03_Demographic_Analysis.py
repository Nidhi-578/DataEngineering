import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    demographic_distribution,
    default_rate_by_demographic,
    default_rate_by_children,
)


st.set_page_config(
    page_title="Demographic Analysis",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading demographic data..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("👥 Customer Demographic Analysis")

st.markdown(
    """
    Analyze the demographic profile of Home Credit applicants
    and identify differences in default risk across customer
    segments.
    """
)


# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("🔎 Demographic Filters")

gender_options = ["All"] + sorted(
    df["CODE_GENDER"].dropna().unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)

if selected_gender != "All":
    filtered_df = df[
        df["CODE_GENDER"] == selected_gender
    ].copy()
else:
    filtered_df = df.copy()


# ============================================================
# KPI CARDS
# ============================================================

total_customers = len(filtered_df)

average_children = filtered_df["CNT_CHILDREN"].mean()

average_family_size = filtered_df[
    "CNT_FAM_MEMBERS"
].mean()

default_rate = filtered_df["TARGET"].mean() * 100


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )


with col2:
    st.metric(
        "Average Children",
        f"{average_children:.2f}"
    )


with col3:
    st.metric(
        "Average Family Size",
        f"{average_family_size:.2f}"
    )


with col4:
    st.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )


# ============================================================
# GENDER DISTRIBUTION
# ============================================================

st.divider()

st.subheader("⚥ Gender Distribution")

gender_data = demographic_distribution(
    filtered_df,
    "CODE_GENDER"
)

fig_gender = px.bar(
    gender_data,
    x="CODE_GENDER",
    y="customers",
    text="customers",
    title="Customers by Gender"
)

fig_gender.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_gender.update_yaxes(
    title="Customers"
)

fig_gender.update_xaxes(
    title="Gender"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ============================================================
# FAMILY STATUS
# ============================================================

st.subheader("💍 Family Status")

family_data = demographic_distribution(
    filtered_df,
    "NAME_FAMILY_STATUS"
)

fig_family = px.bar(
    family_data,
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
# EDUCATION
# ============================================================

st.subheader("🎓 Education Distribution")

education_data = demographic_distribution(
    filtered_df,
    "NAME_EDUCATION_TYPE"
)

fig_education = px.bar(
    education_data,
    x="customers",
    y="NAME_EDUCATION_TYPE",
    orientation="h",
    text="customers",
    title="Customers by Education Level"
)

fig_education.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_education.update_xaxes(
    title="Customers"
)

fig_education.update_yaxes(
    title="Education"
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ============================================================
# HOUSING
# ============================================================

st.subheader("🏠 Housing Type")

housing_data = demographic_distribution(
    filtered_df,
    "NAME_HOUSING_TYPE"
)

fig_housing = px.bar(
    housing_data,
    x="customers",
    y="NAME_HOUSING_TYPE",
    orientation="h",
    text="customers",
    title="Customers by Housing Type"
)

fig_housing.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_housing.update_xaxes(
    title="Customers"
)

fig_housing.update_yaxes(
    title="Housing Type"
)

st.plotly_chart(
    fig_housing,
    use_container_width=True
)


# ============================================================
# CHILDREN DISTRIBUTION
# ============================================================

st.subheader("👨‍👩‍👧 Children Distribution")

children_data = demographic_distribution(
    filtered_df.rename(
        columns={"CNT_CHILDREN": "Children"}
    ),
    "Children"
)

fig_children = px.bar(
    children_data,
    x="Children",
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
# DEFAULT RATE BY GENDER
# ============================================================

st.divider()

st.subheader("⚠️ Default Rate by Gender")

gender_risk = default_rate_by_demographic(
    filtered_df,
    "CODE_GENDER"
)

fig_gender_risk = px.bar(
    gender_risk,
    x="CODE_GENDER",
    y="default_rate",
    text="default_rate",
    title="Default Rate by Gender"
)

fig_gender_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_gender_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_gender_risk,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY FAMILY STATUS
# ============================================================

st.subheader("⚠️ Default Rate by Family Status")

family_risk = default_rate_by_demographic(
    filtered_df,
    "NAME_FAMILY_STATUS"
)

fig_family_risk = px.bar(
    family_risk,
    x="default_rate",
    y="NAME_FAMILY_STATUS",
    orientation="h",
    text="default_rate",
    title="Default Rate by Family Status"
)

fig_family_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_family_risk.update_xaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_family_risk,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY EDUCATION
# ============================================================

st.subheader("⚠️ Default Rate by Education")

education_risk = default_rate_by_demographic(
    filtered_df,
    "NAME_EDUCATION_TYPE"
)

fig_education_risk = px.bar(
    education_risk,
    x="default_rate",
    y="NAME_EDUCATION_TYPE",
    orientation="h",
    text="default_rate",
    title="Default Rate by Education"
)

fig_education_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_education_risk.update_xaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_education_risk,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY CHILDREN
# ============================================================

st.subheader("⚠️ Default Rate by Number of Children")

children_risk = default_rate_by_children(
    filtered_df
)

fig_children_risk = px.bar(
    children_risk,
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
# INSIGHT
# ============================================================

st.divider()

st.subheader("💡 Demographic Insight")

highest_family = family_risk.iloc[0]
highest_education = education_risk.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"""
        **Highest observed family-status default rate**

        {highest_family['NAME_FAMILY_STATUS']}

        Default Rate:
        **{highest_family['default_rate']:.2f}%**
        """
    )

with col2:
    st.info(
        f"""
        **Highest observed education default rate**

        {highest_education['NAME_EDUCATION_TYPE']}

        Default Rate:
        **{highest_education['default_rate']:.2f}%**
        """
    )