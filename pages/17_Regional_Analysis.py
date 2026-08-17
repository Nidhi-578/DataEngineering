import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    region_rating_summary,
    region_city_rating_summary,
    population_region_summary,
    population_density_risk,
    region_financial_summary,
    region_risk_summary,
)


st.set_page_config(
    page_title="Regional Analysis",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading regional analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🌍 Regional & Geographic Risk Analysis")

st.markdown(
    """
    Analyze regional ratings, city-level ratings, population
    density, financial characteristics, and observed default risk.
    """
)


# ============================================================
# REGION RATING SUMMARY
# ============================================================

region_data = region_rating_summary(df)

st.subheader("📊 Regional Rating Overview")

col1, col2, col3 = st.columns(3)

for col, rating in zip(
    [col1, col2, col3],
    [1, 2, 3]
):

    row = region_data[
        region_data["REGION_RATING_CLIENT"] == rating
    ]

    if not row.empty:

        row = row.iloc[0]

        with col:
            st.metric(
                f"Rating {rating} Customers",
                f"{row['customers']:,}"
            )

            st.caption(
                f"Default rate: {row['default_rate']:.2f}%"
            )


# ============================================================
# DEFAULT RATE BY REGION RATING
# ============================================================

st.divider()

st.subheader("⚠️ Default Rate by Region Rating")

fig_region = px.bar(
    region_data,
    x="REGION_RATING_CLIENT",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Client Region Rating"
)

fig_region.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_region.update_xaxes(
    title="Region Rating"
)

fig_region.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


# ============================================================
# REGION + CITY RATING
# ============================================================

st.subheader("🏙️ Region Rating × City Rating")

city_data = region_city_rating_summary(df)

fig_city = px.density_heatmap(
    city_data,
    x="REGION_RATING_CLIENT_W_CITY",
    y="REGION_RATING_CLIENT",
    z="default_rate",
    text_auto=".2f",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Region and City Rating"
)

fig_city.update_xaxes(
    title="Region Rating Within City"
)

fig_city.update_yaxes(
    title="Client Region Rating"
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)


# ============================================================
# POPULATION SUMMARY
# ============================================================

st.divider()

population_summary = population_region_summary(df)

st.subheader("👥 Regional Population Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Relative Population",
        f"{population_summary['average_population_relative']:.5f}"
    )

with col2:
    st.metric(
        "Median",
        f"{population_summary['median_population_relative']:.5f}"
    )

with col3:
    st.metric(
        "Minimum",
        f"{population_summary['minimum_population_relative']:.5f}"
    )

with col4:
    st.metric(
        "Maximum",
        f"{population_summary['maximum_population_relative']:.5f}"
    )


# ============================================================
# POPULATION DENSITY RISK
# ============================================================

population_data = population_density_risk(df)

st.subheader("📍 Default Rate by Population Density")

fig_population = px.bar(
    population_data,
    x="POPULATION_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Relative Population Density"
)

fig_population.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_population.update_xaxes(
    title="Population Density Group"
)

fig_population.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_population,
    use_container_width=True
)


# ============================================================
# FINANCIAL PROFILE
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Region Rating")

financial_data = region_financial_summary(df)

financial_long = financial_data.melt(
    id_vars="REGION_RATING_CLIENT",
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
    x="REGION_RATING_CLIENT",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Region Rating"
)

fig_financial.update_xaxes(
    title="Region Rating"
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# REGIONAL RISK TABLE
# ============================================================

st.divider()

st.subheader("📋 Regional Risk Summary")

risk_data = region_risk_summary(df)

risk_display = risk_data.copy()

risk_display["default_rate"] = (
    risk_display["default_rate"].round(2)
)

st.dataframe(
    risk_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# RISK FILTER
# ============================================================

st.subheader("🔎 Regional Risk Filter")

minimum_customers = st.slider(
    "Minimum customers per regional segment",
    min_value=10,
    max_value=500,
    value=50,
    step=10
)

filtered_risk = risk_data[
    risk_data["customers"] >= minimum_customers
].sort_values(
    "default_rate",
    ascending=False
)

fig_risk = px.bar(
    filtered_risk,
    x="default_rate",
    y="REGION_RATING_CLIENT",
    color="REGION_RATING_CLIENT_W_CITY",
    orientation="h",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Regional Segments by Observed Default Rate"
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_risk.update_xaxes(
    title="Default Rate (%)"
)

fig_risk.update_yaxes(
    title="Client Region Rating"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Regional Insights")

meaningful = risk_data[
    risk_data["customers"] >= 50
]

highest = meaningful.loc[
    meaningful["default_rate"].idxmax()
]

lowest = meaningful.loc[
    meaningful["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:

    st.warning(
        f"""
        **Highest Observed Regional Risk**

        Client Rating:
        **{highest['REGION_RATING_CLIENT']}**

        City Rating:
        **{highest['REGION_RATING_CLIENT_W_CITY']}**

        Default Rate:
        **{highest['default_rate']:.2f}%**

        Customers:
        **{highest['customers']:,}**
        """
    )

with col2:

    st.success(
        f"""
        **Lowest Observed Regional Risk**

        Client Rating:
        **{lowest['REGION_RATING_CLIENT']}**

        City Rating:
        **{lowest['REGION_RATING_CLIENT_W_CITY']}**

        Default Rate:
        **{lowest['default_rate']:.2f}%**

        Customers:
        **{lowest['customers']:,}**
        """
    )


st.caption(
    "Regional ratings and population measures describe observed "
    "patterns in the dataset. Small regional segments should be "
    "interpreted cautiously and these relationships should not "
    "be treated as causal."
)
