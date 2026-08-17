import streamlit as st
import pandas as pd

from utils.analysis import calculate_kpis


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Home Credit Risk Dashboard",
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
    **Home Credit Default Risk Analysis**

    Explore loan applications, customer characteristics,
    and factors associated with credit default.
    """
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# Contract Type
contract_options = ["All"] + sorted(
    df["NAME_CONTRACT_TYPE"].dropna().unique().tolist()
)

selected_contract = st.sidebar.selectbox(
    "Contract Type",
    contract_options
)


# Gender
gender_options = ["All"] + sorted(
    df["CODE_GENDER"].dropna().unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)


# Income Type
income_options = ["All"] + sorted(
    df["NAME_INCOME_TYPE"].dropna().unique().tolist()
)

selected_income = st.sidebar.selectbox(
    "Income Type",
    income_options
)


# Education
education_options = ["All"] + sorted(
    df["NAME_EDUCATION_TYPE"].dropna().unique().tolist()
)

selected_education = st.sidebar.selectbox(
    "Education",
    education_options
)


# Family Status
family_options = ["All"] + sorted(
    df["NAME_FAMILY_STATUS"].dropna().unique().tolist()
)

selected_family = st.sidebar.selectbox(
    "Family Status",
    family_options
)


# Housing Type
housing_options = ["All"] + sorted(
    df["NAME_HOUSING_TYPE"].dropna().unique().tolist()
)

selected_housing = st.sidebar.selectbox(
    "Housing Type",
    housing_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_contract != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_CONTRACT_TYPE"] == selected_contract
    ]


if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["CODE_GENDER"] == selected_gender
    ]


if selected_income != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_INCOME_TYPE"] == selected_income
    ]


if selected_education != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_EDUCATION_TYPE"] == selected_education
    ]


if selected_family != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_FAMILY_STATUS"] == selected_family
    ]


if selected_housing != "All":

    filtered_df = filtered_df[
        filtered_df["NAME_HOUSING_TYPE"] == selected_housing
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

kpis = calculate_kpis(filtered_df)


# ============================================================
# PORTFOLIO KPIs
# ============================================================

st.subheader("📊 Portfolio Overview")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Applications",
        f"{kpis['total_applications']:,}"
    )


with col2:

    st.metric(
        "Defaults",
        f"{kpis['total_defaults']:,}"
    )


with col3:

    st.metric(
        "Default Rate",
        f"{kpis['default_rate']:.2f}%"
    )


with col4:

    st.metric(
        "Avg Income",
        f"₹{kpis['average_income']:,.0f}"
    )


with col5:

    st.metric(
        "Avg Credit",
        f"₹{kpis['average_credit']:,.0f}"
    )


# ============================================================
# FILTER SUMMARY
# ============================================================

st.divider()

st.subheader("📋 Filter Summary")

st.write(
    f"Showing **{len(filtered_df):,}** applications "
    f"out of **{len(df):,}** total applications."
)


# ============================================================
# APPLICATION DATA
# ============================================================

st.divider()

st.subheader("🔍 Application Data")


display_columns = [
    "SK_ID_CURR",
    "TARGET",
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE"
]


st.dataframe(
    filtered_df[display_columns].head(100),
    use_container_width=True,
    hide_index=True
)