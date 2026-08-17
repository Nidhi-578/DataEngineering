import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    housing_type_summary,
    car_ownership_summary,
    realty_ownership_summary,
    car_age_summary,
    car_age_risk_summary,
    housing_financial_summary,
    asset_ownership_summary,
)


st.set_page_config(
    page_title="Housing & Assets",
    page_icon="🏠",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading housing and asset analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🏠 Housing & Assets Analysis")

st.markdown(
    """
    Analyze housing type, car ownership, realty ownership,
    car age, financial characteristics, and observed default risk.
    """
)


# ============================================================
# OWNERSHIP KPIs
# ============================================================

car_summary = car_ownership_summary(df)
realty_summary = realty_ownership_summary(df)
car_age = car_age_summary(df)

car_owner_count = int(
    car_summary.loc[
        car_summary["FLAG_OWN_CAR"] == "Y",
        "customers"
    ].sum()
)

realty_owner_count = int(
    realty_summary.loc[
        realty_summary["FLAG_OWN_REALTY"] == "Y",
        "customers"
    ].sum()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Car Owners",
        f"{car_owner_count:,}"
    )

with col2:
    st.metric(
        "Realty Owners",
        f"{realty_owner_count:,}"
    )

with col3:
    st.metric(
        "Average Car Age",
        f"{car_age['average_car_age']:.1f} years"
    )

with col4:
    st.metric(
        "Median Car Age",
        f"{car_age['median_car_age']:.0f} years"
    )


# ============================================================
# HOUSING DISTRIBUTION
# ============================================================

st.divider()

st.subheader("🏠 Housing Type Distribution")

housing_data = housing_type_summary(df)

fig_housing = px.bar(
    housing_data,
    x="NAME_HOUSING_TYPE",
    y="customers",
    text="customers",
    title="Customers by Housing Type"
)

fig_housing.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_housing.update_xaxes(
    title="Housing Type",
    tickangle=-25
)

fig_housing.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_housing,
    use_container_width=True
)


# ============================================================
# HOUSING DEFAULT RATE
# ============================================================

st.subheader("⚠️ Default Rate by Housing Type")

fig_housing_risk = px.bar(
    housing_data,
    x="NAME_HOUSING_TYPE",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Housing Type"
)

fig_housing_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_housing_risk.update_xaxes(
    title="Housing Type",
    tickangle=-25
)

fig_housing_risk.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_housing_risk,
    use_container_width=True
)


# ============================================================
# CAR VS REALTY OWNERSHIP
# ============================================================

st.divider()

st.subheader("🚗 Car Ownership")

col1, col2 = st.columns(2)

with col1:

    fig_car = px.bar(
        car_summary,
        x="FLAG_OWN_CAR",
        y="customers",
        text="customers",
        title="Customers by Car Ownership"
    )

    fig_car.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig_car.update_xaxes(
        tickmode="array",
        tickvals=["N", "Y"],
        ticktext=["No Car", "Own Car"]
    )

    fig_car.update_yaxes(
        title="Customers"
    )

    st.plotly_chart(
        fig_car,
        use_container_width=True
    )


with col2:

    fig_car_risk = px.bar(
        car_summary,
        x="FLAG_OWN_CAR",
        y="default_rate",
        text="default_rate",
        title="Default Rate by Car Ownership"
    )

    fig_car_risk.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_car_risk.update_xaxes(
        tickmode="array",
        tickvals=["N", "Y"],
        ticktext=["No Car", "Own Car"]
    )

    fig_car_risk.update_yaxes(
        title="Default Rate (%)"
    )

    st.plotly_chart(
        fig_car_risk,
        use_container_width=True
    )


# ============================================================
# REALTY OWNERSHIP
# ============================================================

st.subheader("🏡 Realty Ownership")

col1, col2 = st.columns(2)

with col1:

    fig_realty = px.bar(
        realty_summary,
        x="FLAG_OWN_REALTY",
        y="customers",
        text="customers",
        title="Customers by Realty Ownership"
    )

    fig_realty.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig_realty.update_xaxes(
        tickmode="array",
        tickvals=["N", "Y"],
        ticktext=["No Realty", "Own Realty"]
    )

    fig_realty.update_yaxes(
        title="Customers"
    )

    st.plotly_chart(
        fig_realty,
        use_container_width=True
    )


with col2:

    fig_realty_risk = px.bar(
        realty_summary,
        x="FLAG_OWN_REALTY",
        y="default_rate",
        text="default_rate",
        title="Default Rate by Realty Ownership"
    )

    fig_realty_risk.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_realty_risk.update_xaxes(
        tickmode="array",
        tickvals=["N", "Y"],
        ticktext=["No Realty", "Own Realty"]
    )

    fig_realty_risk.update_yaxes(
        title="Default Rate (%)"
    )

    st.plotly_chart(
        fig_realty_risk,
        use_container_width=True
    )


# ============================================================
# CAR AGE
# ============================================================

st.divider()

st.subheader("🚘 Car Age Analysis")

car_age_risk = car_age_risk_summary(df)

fig_car_age = px.bar(
    car_age_risk,
    x="CAR_AGE_GROUP",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Car Age"
)

fig_car_age.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_car_age.update_xaxes(
    title="Car Age"
)

fig_car_age.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_car_age,
    use_container_width=True
)


# ============================================================
# HOUSING FINANCIAL PROFILE
# ============================================================

st.divider()

st.subheader("💰 Financial Profile by Housing Type")

housing_financial = housing_financial_summary(df)

financial_long = housing_financial.melt(
    id_vars="NAME_HOUSING_TYPE",
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
    x="NAME_HOUSING_TYPE",
    y="average_value",
    color="metric",
    barmode="group",
    title="Average Income, Credit and Annuity by Housing Type"
)

fig_financial.update_xaxes(
    title="Housing Type",
    tickangle=-25
)

fig_financial.update_yaxes(
    title="Average Amount"
)

st.plotly_chart(
    fig_financial,
    use_container_width=True
)


# ============================================================
# ASSET OWNERSHIP COMBINATION
# ============================================================

st.divider()

st.subheader("🚗🏡 Asset Ownership Combination")

asset_data = asset_ownership_summary(df)

asset_data["SEGMENT"] = (
    asset_data["CAR_OWNER"]
    + " + "
    + asset_data["REALTY_OWNER"]
)

fig_asset = px.bar(
    asset_data,
    x="SEGMENT",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Car & Realty Ownership"
)

fig_asset.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_asset.update_xaxes(
    title="Asset Ownership Segment"
)

fig_asset.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_asset,
    use_container_width=True
)


# ============================================================
# ASSET TABLE
# ============================================================

st.subheader("📋 Asset Ownership Risk Summary")

display_asset = asset_data.copy()

display_asset["default_rate"] = (
    display_asset["default_rate"].round(2)
)

st.dataframe(
    display_asset,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Housing & Asset Insights")

meaningful_housing = housing_data[
    housing_data["customers"] >= 50
]

highest_housing_risk = meaningful_housing.loc[
    meaningful_housing["default_rate"].idxmax()
]

lowest_housing_risk = meaningful_housing.loc[
    meaningful_housing["default_rate"].idxmin()
]

highest_asset_risk = asset_data.loc[
    asset_data["default_rate"].idxmax()
]

lowest_asset_risk = asset_data.loc[
    asset_data["default_rate"].idxmin()
]


col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"""
        **Highest Observed Housing Risk**

        {highest_housing_risk['NAME_HOUSING_TYPE']}

        Default Rate:
        **{highest_housing_risk['default_rate']:.2f}%**

        Customers:
        **{highest_housing_risk['customers']:,}**
        """
    )

with col2:
    st.info(
        f"""
        **Highest Asset-Combination Default Rate**

        {highest_asset_risk['SEGMENT']}

        Default Rate:
        **{highest_asset_risk['default_rate']:.2f}%**

        Customers:
        **{highest_asset_risk['customers']:,}**
        """
    )


st.caption(
    "Default rates describe observed patterns in the dataset. "
    "Small housing or asset segments should be interpreted "
    "cautiously and these relationships should not be treated "
    "as causal."
)