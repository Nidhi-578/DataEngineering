import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analysis import (
    external_score_summary,
    external_score_default_summary,
    external_score_band_risk,
    combined_external_score,
    combined_score_risk,
)


st.set_page_config(
    page_title="External Credit Score",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/application_train.csv")


with st.spinner("Loading external credit score analysis..."):
    df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("📈 External Credit Score Analysis")

st.markdown(
    """
    Analyze external credit scores and their relationship with
    observed loan default risk.
    """
)


# ============================================================
# SCORE SUMMARY
# ============================================================

score_summary = external_score_summary(df)

st.subheader("📊 External Score Overview")

col1, col2, col3 = st.columns(3)

for col, score_name in zip(
    [col1, col2, col3],
    [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]
):

    row = score_summary[
        score_summary["score"] == score_name
    ].iloc[0]

    with col:
        st.metric(
            score_name,
            f"{row['average']:.3f}"
        )

        st.caption(
            f"Available: {row['available']:,} customers"
        )


# ============================================================
# SCORE DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📉 External Score Distribution")

score_columns = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]

selected_score = st.selectbox(
    "Select external score",
    score_columns
)

score_data = df[
    [selected_score]
].dropna()

fig_distribution = px.histogram(
    score_data,
    x=selected_score,
    nbins=30,
    title=f"{selected_score} Distribution"
)

fig_distribution.update_xaxes(
    title="Score"
)

fig_distribution.update_yaxes(
    title="Customers"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# DEFAULT VS NON-DEFAULT
# ============================================================

st.subheader("⚠️ Default vs Non-Default Average Scores")

default_comparison = external_score_default_summary(df)

comparison_long = default_comparison.melt(
    id_vars="score",
    value_vars=[
        "default_average",
        "non_default_average"
    ],
    var_name="customer_type",
    value_name="average_score"
)

comparison_long["customer_type"] = (
    comparison_long["customer_type"].map(
        {
            "default_average": "Default",
            "non_default_average": "Non-Default"
        }
    )
)

fig_comparison = px.bar(
    comparison_long,
    x="score",
    y="average_score",
    color="customer_type",
    barmode="group",
    text="average_score",
    title="Average External Scores: Default vs Non-Default"
)

fig_comparison.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)

fig_comparison.update_xaxes(
    title="External Score"
)

fig_comparison.update_yaxes(
    title="Average Score"
)

st.plotly_chart(
    fig_comparison,
    use_container_width=True
)


# ============================================================
# SCORE BAND RISK
# ============================================================

st.divider()

st.subheader("🔎 Default Rate by External Score Band")

band_data = external_score_band_risk(df)

selected_band_score = st.selectbox(
    "Select score for risk analysis",
    score_columns,
    key="band_score"
)

selected_band_data = band_data[
    band_data["score"] == selected_band_score
]

fig_band = px.bar(
    selected_band_data,
    x="SCORE_BAND",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title=f"Default Rate by {selected_band_score} Band"
)

fig_band.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_band.update_xaxes(
    title="Score Band"
)

fig_band.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_band,
    use_container_width=True
)


# ============================================================
# ALL SCORE BANDS
# ============================================================

st.subheader("📊 External Score Risk Comparison")

fig_all_bands = px.line(
    band_data,
    x="SCORE_BAND",
    y="default_rate",
    color="score",
    markers=True,
    title="Default Rate Across External Score Bands"
)

fig_all_bands.update_xaxes(
    title="Score Band"
)

fig_all_bands.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_all_bands,
    use_container_width=True
)


# ============================================================
# COMBINED SCORE
# ============================================================

st.divider()

st.subheader("🎯 Combined External Credit Score")

combined_data = combined_score_risk(df)

fig_combined = px.bar(
    combined_data,
    x="COMBINED_SCORE_BAND",
    y="default_rate",
    text="default_rate",
    hover_data=[
        "customers",
        "defaults"
    ],
    title="Default Rate by Combined External Score"
)

fig_combined.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_combined.update_xaxes(
    title="Combined External Score"
)

fig_combined.update_yaxes(
    title="Default Rate (%)"
)

st.plotly_chart(
    fig_combined,
    use_container_width=True
)


# ============================================================
# COMBINED SCORE TABLE
# ============================================================

st.subheader("📋 Combined Score Risk Summary")

combined_display = combined_data.copy()

combined_display["default_rate"] = (
    combined_display["default_rate"].round(2)
)

st.dataframe(
    combined_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SCORE AVAILABILITY
# ============================================================

st.divider()

st.subheader("📌 External Score Availability")

availability = score_summary[
    [
        "score",
        "available"
    ]
].copy()

availability["missing"] = (
    len(df) -
    availability["available"]
)

availability["availability_rate"] = (
    availability["available"] /
    len(df) *
    100
)

availability["availability_rate"] = (
    availability["availability_rate"].round(2)
)

st.dataframe(
    availability,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# KEY INSIGHT
# ============================================================

st.subheader("💡 Key External Score Insight")

meaningful_combined = combined_data[
    combined_data["customers"] >= 50
]

highest_risk = meaningful_combined.loc[
    meaningful_combined["default_rate"].idxmax()
]

lowest_risk = meaningful_combined.loc[
    meaningful_combined["default_rate"].idxmin()
]

col1, col2 = st.columns(2)

with col1:

    st.warning(
        f"""
        **Highest Observed Combined-Score Risk**

        Score Band:
        **{highest_risk['COMBINED_SCORE_BAND']}**

        Default Rate:
        **{highest_risk['default_rate']:.2f}%**

        Customers:
        **{highest_risk['customers']:,}**
        """
    )

with col2:

    st.success(
        f"""
        **Lowest Observed Meaningful Score Risk**

        Score Band:
        **{lowest_risk['COMBINED_SCORE_BAND']}**

        Default Rate:
        **{lowest_risk['default_rate']:.2f}%**

        Customers:
        **{lowest_risk['customers']:,}**
        """
    )


st.caption(
    "External scores are not available for every customer. "
    "Combined scores use the available external scores. "
    "Default rates describe observed patterns and should not "
    "be interpreted as causal relationships. Small score bands "
    "should be interpreted cautiously."
)