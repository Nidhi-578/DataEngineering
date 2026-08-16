import streamlit as st
import pandas as pd


def apply_filters(df):
    """
    Apply common dashboard filters across all pages.

    Filters:
    - Order Date
    - Region
    - State/Province
    - Segment
    - Category
    - Sub-Category
    - Ship Mode
    """

    # ========================================================
    # SIDEBAR HEADER
    # ========================================================

    st.sidebar.title("🎛️ Dashboard Filters")

    st.sidebar.caption(
        "Use the filters below to analyze a specific "
        "part of the Superstore dataset."
    )

    # ========================================================
    # RESET FILTERS
    # ========================================================

    if st.sidebar.button(
        "🔄 Reset Filters",
        width="stretch"
    ):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    # ========================================================
    # MAKE SURE ORDER DATE IS DATETIME
    # ========================================================

    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(
        df["Order Date"]
    ):
        df["Order Date"] = pd.to_datetime(
            df["Order Date"]
        )

    # ========================================================
    # DATE RANGE
    # ========================================================

    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()

    date_range = st.sidebar.date_input(
        "📅 Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="filter_date_range"
    )

    # ========================================================
    # REGION
    # ========================================================

    regions = sorted(
        df["Region"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_regions = st.sidebar.multiselect(
        "🌎 Region",
        options=regions,
        default=regions,
        key="filter_regions"
    )

    # ========================================================
    # STATE
    # ========================================================

    states = sorted(
        df["State/Province"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_states = st.sidebar.multiselect(
        "📍 State / Province",
        options=states,
        default=states,
        key="filter_states"
    )

    # ========================================================
    # SEGMENT
    # ========================================================

    segments = sorted(
        df["Segment"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_segments = st.sidebar.multiselect(
        "👥 Segment",
        options=segments,
        default=segments,
        key="filter_segments"
    )

    # ========================================================
    # CATEGORY
    # ========================================================

    categories = sorted(
        df["Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "📦 Category",
        options=categories,
        default=categories,
        key="filter_categories"
    )

    # ========================================================
    # SUB-CATEGORY
    # ========================================================

    sub_categories = sorted(
        df["Sub-Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_sub_categories = st.sidebar.multiselect(
        "🏷️ Sub-Category",
        options=sub_categories,
        default=sub_categories,
        key="filter_sub_categories"
    )

    # ========================================================
    # SHIP MODE
    # ========================================================

    ship_modes = sorted(
        df["Ship Mode"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_ship_modes = st.sidebar.multiselect(
        "🚚 Ship Mode",
        options=ship_modes,
        default=ship_modes,
        key="filter_ship_modes"
    )

    # ========================================================
    # APPLY NON-DATE FILTERS
    # ========================================================

    filtered_df = df[
        df["Region"].isin(selected_regions)
        & df["State/Province"].isin(selected_states)
        & df["Segment"].isin(selected_segments)
        & df["Category"].isin(selected_categories)
        & df["Sub-Category"].isin(selected_sub_categories)
        & df["Ship Mode"].isin(selected_ship_modes)
    ].copy()

    # ========================================================
    # APPLY DATE FILTER
    # ========================================================

    if (
        isinstance(date_range, tuple)
        and len(date_range) == 2
    ):

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (
                filtered_df["Order Date"].dt.date
                >= start_date
            )
            &
            (
                filtered_df["Order Date"].dt.date
                <= end_date
            )
        ]

    # ========================================================
    # SIDEBAR FILTER SUMMARY
    # ========================================================

    st.sidebar.markdown("---")

    st.sidebar.subheader("📊 Filter Summary")

    st.sidebar.metric(
        "Records",
        f"{len(filtered_df):,}"
    )

    if len(df) > 0:

        percentage = (
            len(filtered_df)
            / len(df)
            * 100
        )

        st.sidebar.caption(
            f"{percentage:.1f}% of original data"
        )

    return filtered_df