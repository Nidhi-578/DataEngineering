import pandas as pd
import numpy as np


def calculate_kpis(df):
    """Calculate high-level portfolio KPIs."""

    total_applications = len(df)

    total_defaults = (df["TARGET"] == 1).sum()

    default_rate = (
        total_defaults / total_applications * 100
        if total_applications > 0
        else 0
    )

    average_income = df["AMT_INCOME_TOTAL"].mean()
    average_credit = df["AMT_CREDIT"].mean()
    average_annuity = df["AMT_ANNUITY"].mean()

    return {
        "total_applications": total_applications,
        "total_defaults": total_defaults,
        "default_rate": default_rate,
        "average_income": average_income,
        "average_credit": average_credit,
        "average_annuity": average_annuity,
    }


def default_summary(df):
    """Return default vs non-default customer counts."""

    result = (
        df["TARGET"]
        .map({
            0: "Non-Default",
            1: "Default"
        })
        .value_counts()
        .reset_index()
    )

    result.columns = ["status", "customers"]

    return result


def applications_by_category(df, column):
    """Return application count by category."""

    return (
        df[column]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
        .rename(
            columns={
                column: "category",
                "count": "applications"
            }
        )
    )


def credit_statistics(df):
    """Calculate credit amount statistics."""

    return {
        "total_credit": df["AMT_CREDIT"].sum(),
        "average_credit": df["AMT_CREDIT"].mean(),
        "median_credit": df["AMT_CREDIT"].median(),
        "minimum_credit": df["AMT_CREDIT"].min(),
        "maximum_credit": df["AMT_CREDIT"].max(),
    }


def executive_insights(df):
    """Generate key business insights."""

    total_applications = len(df)

    default_rate = (
        df["TARGET"].mean() * 100
        if total_applications > 0
        else 0
    )

    average_income = df["AMT_INCOME_TOTAL"].mean()
    average_credit = df["AMT_CREDIT"].mean()

    most_common_income = (
        df["NAME_INCOME_TYPE"]
        .value_counts()
        .idxmax()
    )

    most_common_education = (
        df["NAME_EDUCATION_TYPE"]
        .value_counts()
        .idxmax()
    )

    risk_by_income = (
        df.groupby("NAME_INCOME_TYPE")["TARGET"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_risk_segment = risk_by_income.index[0]

    return {
        "default_rate": default_rate,
        "average_income": average_income,
        "average_credit": average_credit,
        "most_common_income": most_common_income,
        "most_common_education": most_common_education,
        "highest_risk_segment": highest_risk_segment,
    }
def prepare_customer_data(df):
    """
    Create business-friendly customer attributes.
    """

    result = df.copy()

    # Age in years
    result["AGE"] = (
        result["DAYS_BIRTH"].abs() / 365.25
    )

    # Age groups
    result["AGE_GROUP"] = pd.cut(
        result["AGE"],
        bins=[0, 25, 35, 45, 55, 65, 100],
        labels=[
            "18-25",
            "26-35",
            "36-45",
            "46-55",
            "56-65",
            "65+"
        ],
        include_lowest=True
    )

    # Income groups
    result["INCOME_GROUP"] = pd.qcut(
        result["AMT_INCOME_TOTAL"],
        q=4,
        labels=[
            "Low Income",
            "Lower-Middle Income",
            "Upper-Middle Income",
            "High Income"
        ],
        duplicates="drop"
    )

    # Credit-to-income ratio
    result["CREDIT_INCOME_RATIO"] = (
        result["AMT_CREDIT"] /
        result["AMT_INCOME_TOTAL"]
    )

    return result


def default_rate_by_age_group(df):
    """
    Calculate default rate by age group.
    """

    result = (
        df.groupby(
            "AGE_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def default_rate_by_income_type(df):
    """
    Calculate default rate by income type.
    """

    result = (
        df.groupby("NAME_INCOME_TYPE")["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def default_rate_by_education(df):
    """
    Calculate default rate by education.
    """

    result = (
        df.groupby("NAME_EDUCATION_TYPE")["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def default_rate_by_family_status(df):
    """
    Calculate default rate by family status.
    """

    result = (
        df.groupby("NAME_FAMILY_STATUS")["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def default_rate_by_housing(df):
    """
    Calculate default rate by housing type.
    """

    result = (
        df.groupby("NAME_HOUSING_TYPE")["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def default_rate_by_occupation(df):
    """
    Calculate default rate by occupation.
    """

    result = (
        df.groupby("OCCUPATION_TYPE")["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )
def default_rate_by_column(df, column):
    """
    Calculate application count, defaults, and default rate
    for a categorical column.
    """

    result = (
        df.groupby(column, dropna=False)["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] = result["default_rate"] * 100

    result[column] = result[column].fillna("Unknown")

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def default_rate_by_gender(df):
    """Calculate default rate by gender."""
    return default_rate_by_column(
        df,
        "CODE_GENDER"
    )


def default_rate_by_contract(df):
    """Calculate default rate by contract type."""
    return default_rate_by_column(
        df,
        "NAME_CONTRACT_TYPE"
    )


def external_score_analysis(df):
    """
    Analyze external credit scores and default rates.
    """

    score_columns = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    results = []

    for column in score_columns:

        score_data = df[
            [column, "TARGET"]
        ].dropna()

        if len(score_data) == 0:
            continue

        default_score = score_data.loc[
            score_data["TARGET"] == 1,
            column
        ].mean()

        non_default_score = score_data.loc[
            score_data["TARGET"] == 0,
            column
        ].mean()

        results.append(
            {
                "score": column,
                "default_average": default_score,
                "non_default_average": non_default_score,
            }
        )

    return pd.DataFrame(results)


def financial_risk_summary(df):
    """
    Compare financial characteristics between
    default and non-default customers.
    """

    result = (
        df.groupby("TARGET")[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY",
                "CREDIT_INCOME_RATIO"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["TARGET"] = result["TARGET"].map(
        {
            0: "Non-Default",
            1: "Default"
        }
    )

    return result


def credit_income_risk(df):
    """
    Analyze default rate across credit-to-income
    ratio segments.
    """

    data = df[
        "CREDIT_INCOME_RATIO"
    ].replace(
        [float("inf"), -float("inf")],
        pd.NA
    ).dropna()

    working_df = df.loc[data.index].copy()

    working_df["RATIO_GROUP"] = pd.cut(
        working_df["CREDIT_INCOME_RATIO"],
        bins=[
            0,
            2,
            4,
            6,
            10,
            float("inf")
        ],
        labels=[
            "< 2x",
            "2x - 4x",
            "4x - 6x",
            "6x - 10x",
            "10x+"
        ]
    )

    result = (
        working_df.groupby(
            "RATIO_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def risk_segment_summary(df):
    """
    Create simple risk segments based on
    external credit scores and credit-to-income ratio.
    """

    working_df = df.copy()

    score_columns = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    working_df["AVG_EXTERNAL_SCORE"] = (
        working_df[score_columns]
        .mean(axis=1)
    )

    working_df["RISK_SCORE"] = (
        working_df["AVG_EXTERNAL_SCORE"] -
        (
            working_df["CREDIT_INCOME_RATIO"]
            .clip(upper=20) / 20
        )
    )

    working_df["RISK_SEGMENT"] = pd.cut(
        working_df["RISK_SCORE"],
        bins=[
            -float("inf"),
            0.20,
            0.40,
            float("inf")
        ],
        labels=[
            "High Risk",
            "Medium Risk",
            "Low Risk"
        ]
    )

    result = (
        working_df.groupby(
            "RISK_SEGMENT",
            observed=False
        )["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result
def target_summary(df):
    """
    Summary of TARGET distribution.
    TARGET = 0 -> Non-Default
    TARGET = 1 -> Default
    """

    total_customers = len(df)

    default_customers = (df["TARGET"] == 1).sum()
    non_default_customers = (df["TARGET"] == 0).sum()

    default_rate = (
        default_customers / total_customers * 100
        if total_customers > 0
        else 0
    )

    non_default_rate = (
        non_default_customers / total_customers * 100
        if total_customers > 0
        else 0
    )

    return {
        "total_customers": total_customers,
        "default_customers": default_customers,
        "non_default_customers": non_default_customers,
        "default_rate": default_rate,
        "non_default_rate": non_default_rate,
    }
def demographic_distribution(df, column):
    """
    Return customer count by demographic category.
    """

    result = (
        df[column]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    result.columns = [
        column,
        "customers"
    ]

    return result


def default_rate_by_demographic(df, column):
    """
    Calculate customers, defaults and default rate
    for a demographic column.
    """

    result = (
        df.groupby(
            column,
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result[column] = result[column].fillna("Unknown")

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def children_distribution(df):
    """
    Customer distribution by number of children.
    """

    result = (
        df.groupby("CNT_CHILDREN")["SK_ID_CURR"]
        .count()
        .reset_index()
    )

    result.columns = [
        "children",
        "customers"
    ]

    return result.sort_values("children")


def default_rate_by_children(df):
    """
    Default rate by number of children.
    """

    result = (
        df.groupby("CNT_CHILDREN")["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values("CNT_CHILDREN")
def age_distribution(df):
    """
    Return customer count by age group.
    """

    result = (
        df["AGE_GROUP"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    result.columns = [
        "AGE_GROUP",
        "customers"
    ]

    return result


def default_rate_by_age(df):
    """
    Calculate customer count, defaults and default rate
    by age group.
    """

    result = (
        df.groupby(
            "AGE_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def age_financial_summary(df):
    """
    Compare average income, credit and annuity
    across age groups.
    """

    result = (
        df.groupby(
            "AGE_GROUP",
            observed=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    return result
def gender_summary(df):
    """
    Customer count and percentage by gender.
    """

    result = (
        df["CODE_GENDER"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "gender",
        "customers"
    ]

    result["percentage"] = (
        result["customers"] /
        result["customers"].sum() * 100
    )

    return result


def gender_financial_summary(df):
    """
    Average income, credit and annuity by gender.
    """

    result = (
        df.groupby(
            "CODE_GENDER",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["CODE_GENDER"] = (
        result["CODE_GENDER"]
        .fillna("Unknown")
    )

    return result


def gender_default_summary(df):
    """
    Default count and default rate by gender.
    """

    result = (
        df.groupby(
            "CODE_GENDER",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["CODE_GENDER"] = (
        result["CODE_GENDER"]
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result


def gender_education_risk(df):
    """
    Default rate by gender and education.
    """

    result = (
        df.groupby(
            [
                "CODE_GENDER",
                "NAME_EDUCATION_TYPE"
            ],
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    result["CODE_GENDER"] = (
        result["CODE_GENDER"]
        .fillna("Unknown")
    )

    result["NAME_EDUCATION_TYPE"] = (
        result["NAME_EDUCATION_TYPE"]
        .fillna("Unknown")
    )

    return result


def gender_income_risk(df):
    """
    Default rate by gender and income type.
    """

    result = (
        df.groupby(
            [
                "CODE_GENDER",
                "NAME_INCOME_TYPE"
            ],
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    result["CODE_GENDER"] = (
        result["CODE_GENDER"]
        .fillna("Unknown")
    )

    result["NAME_INCOME_TYPE"] = (
        result["NAME_INCOME_TYPE"]
        .fillna("Unknown")
    )

    return result
def income_summary(df):
    """
    Overall income statistics.
    """

    return {
        "total_income": df["AMT_INCOME_TOTAL"].sum(),
        "average_income": df["AMT_INCOME_TOTAL"].mean(),
        "median_income": df["AMT_INCOME_TOTAL"].median(),
        "minimum_income": df["AMT_INCOME_TOTAL"].min(),
        "maximum_income": df["AMT_INCOME_TOTAL"].max(),
    }


def income_group_distribution(df):
    """
    Customer distribution by income group.
    """

    result = (
        df["INCOME_GROUP"]
        .astype("object")
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "INCOME_GROUP",
        "customers"
    ]

    return result


def default_rate_by_income_group(df):
    """
    Default rate by income group.
    """

    result = (
        df.groupby(
            "INCOME_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def income_type_summary(df):
    """
    Customer distribution and default rate by income type.
    """

    result = (
        df.groupby(
            "NAME_INCOME_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["NAME_INCOME_TYPE"] = (
        result["NAME_INCOME_TYPE"]
        .fillna("Unknown")
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def income_credit_summary(df):
    """
    Average credit and annuity by income group.
    """

    result = (
        df.groupby(
            "INCOME_GROUP",
            observed=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    return result
def credit_group_distribution(df):
    """
    Customer distribution by credit amount group.
    """

    result = pd.cut(
        df["AMT_CREDIT"],
        bins=[
            0,
            250000,
            500000,
            750000,
            1000000,
            float("inf")
        ],
        labels=[
            "<250K",
            "250K-500K",
            "500K-750K",
            "750K-1M",
            "1M+"
        ]
    )

    result = (
        result
        .value_counts()
        .sort_index()
        .reset_index()
    )

    result.columns = [
        "CREDIT_GROUP",
        "customers"
    ]

    return result


def default_rate_by_credit_group(df):
    """
    Default rate by credit amount group.
    """

    data = df.copy()

    data["CREDIT_GROUP"] = pd.cut(
        data["AMT_CREDIT"],
        bins=[
            0,
            250000,
            500000,
            750000,
            1000000,
            float("inf")
        ],
        labels=[
            "<250K",
            "250K-500K",
            "500K-750K",
            "750K-1M",
            "1M+"
        ]
    )

    result = (
        data.groupby(
            "CREDIT_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def credit_income_summary(df):
    """
    Credit-to-income statistics.
    """

    ratio = (
        df["AMT_CREDIT"] /
        df["AMT_INCOME_TOTAL"]
    )

    return {
        "average_ratio": ratio.mean(),
        "median_ratio": ratio.median(),
        "minimum_ratio": ratio.min(),
        "maximum_ratio": ratio.max(),
    }
def annuity_summary(df):
    """
    Overall annuity statistics.
    """

    return {
        "total_annuity": df["AMT_ANNUITY"].sum(),
        "average_annuity": df["AMT_ANNUITY"].mean(),
        "median_annuity": df["AMT_ANNUITY"].median(),
        "minimum_annuity": df["AMT_ANNUITY"].min(),
        "maximum_annuity": df["AMT_ANNUITY"].max(),
    }


def annuity_income_summary(df):
    """
    Calculate annuity-to-income ratio statistics.
    """

    ratio = (
        df["AMT_ANNUITY"] /
        df["AMT_INCOME_TOTAL"]
    )

    return {
        "average_ratio": ratio.mean(),
        "median_ratio": ratio.median(),
        "minimum_ratio": ratio.min(),
        "maximum_ratio": ratio.max(),
    }


def annuity_burden_distribution(df):
    """
    Customer distribution by annuity-to-income burden.
    """

    data = df.copy()

    data["ANNUITY_BURDEN"] = pd.cut(
        data["AMT_ANNUITY"] /
        data["AMT_INCOME_TOTAL"],
        bins=[
            0,
            0.10,
            0.20,
            0.30,
            0.40,
            float("inf")
        ],
        labels=[
            "<10%",
            "10%-20%",
            "20%-30%",
            "30%-40%",
            "40%+"
        ]
    )

    result = (
        data["ANNUITY_BURDEN"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    result.columns = [
        "ANNUITY_BURDEN",
        "customers"
    ]

    return result


def default_rate_by_annuity_burden(df):
    """
    Default rate by annuity-to-income burden.
    """

    data = df.copy()

    data["ANNUITY_BURDEN"] = pd.cut(
        data["AMT_ANNUITY"] /
        data["AMT_INCOME_TOTAL"],
        bins=[
            0,
            0.10,
            0.20,
            0.30,
            0.40,
            float("inf")
        ],
        labels=[
            "<10%",
            "10%-20%",
            "20%-30%",
            "30%-40%",
            "40%+"
        ]
    )

    result = (
        data.groupby(
            "ANNUITY_BURDEN",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result
def income_credit_segment_summary(df):
    """
    Analyze default risk across income groups and
    credit amount groups.
    """

    data = df.copy()

    data["CREDIT_GROUP"] = pd.cut(
        data["AMT_CREDIT"],
        bins=[
            0,
            250000,
            500000,
            750000,
            1000000,
            float("inf")
        ],
        labels=[
            "<250K",
            "250K-500K",
            "500K-750K",
            "750K-1M",
            "1M+"
        ]
    )

    result = (
        data.groupby(
            [
                "INCOME_GROUP",
                "CREDIT_GROUP"
            ],
            observed=False
        )["TARGET"]
        .agg(
            applications="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def high_credit_low_income_summary(df):
    """
    Identify customers with relatively high credit
    compared with their income.

    High credit = credit-to-income ratio >= 6x.
    """

    data = df.copy()

    data["CREDIT_INCOME_RATIO"] = (
        data["AMT_CREDIT"] /
        data["AMT_INCOME_TOTAL"]
    )

    result = data[
        data["CREDIT_INCOME_RATIO"] >= 6
    ].copy()

    return {
        "customers": len(result),
        "defaults": int(result["TARGET"].sum()),
        "default_rate": result["TARGET"].mean() * 100
        if len(result) > 0 else 0,
        "average_income": result["AMT_INCOME_TOTAL"].mean()
        if len(result) > 0 else 0,
        "average_credit": result["AMT_CREDIT"].mean()
        if len(result) > 0 else 0,
        "average_ratio": result["CREDIT_INCOME_RATIO"].mean()
        if len(result) > 0 else 0,
    }
def high_annuity_burden_summary(df):
    """
    Analyze customers with high annuity-to-income burden.

    High burden = annuity is at least 30% of income.
    """

    data = df.copy()

    data["ANNUITY_INCOME_RATIO"] = (
        data["AMT_ANNUITY"] /
        data["AMT_INCOME_TOTAL"]
    )

    result = data[
        data["ANNUITY_INCOME_RATIO"] >= 0.30
    ].copy()

    return {
        "customers": len(result),
        "defaults": int(result["TARGET"].sum()),
        "default_rate": (
            result["TARGET"].mean() * 100
            if len(result) > 0
            else 0
        ),
        "average_income": (
            result["AMT_INCOME_TOTAL"].mean()
            if len(result) > 0
            else 0
        ),
        "average_annuity": (
            result["AMT_ANNUITY"].mean()
            if len(result) > 0
            else 0
        ),
        "average_ratio": (
            result["ANNUITY_INCOME_RATIO"].mean()
            if len(result) > 0
            else 0
        ),
    }
def education_distribution(df):
    """
    Customer distribution by education level.
    """

    result = (
        df["NAME_EDUCATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "education",
        "customers"
    ]

    return result


def education_default_summary(df):
    """
    Default count and default rate by education level.
    """

    result = (
        df.groupby(
            "NAME_EDUCATION_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["NAME_EDUCATION_TYPE"] = (
        result["NAME_EDUCATION_TYPE"]
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def education_financial_summary(df):
    """
    Average income, credit and annuity by education level.
    """

    result = (
        df.groupby(
            "NAME_EDUCATION_TYPE",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["NAME_EDUCATION_TYPE"] = (
        result["NAME_EDUCATION_TYPE"]
        .fillna("Unknown")
    )

    return result


def education_income_risk(df):
    """
    Default rate by education and income type.
    """

    result = (
        df.groupby(
            [
                "NAME_EDUCATION_TYPE",
                "NAME_INCOME_TYPE"
            ],
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["NAME_EDUCATION_TYPE"] = (
        result["NAME_EDUCATION_TYPE"]
        .fillna("Unknown")
    )

    result["NAME_INCOME_TYPE"] = (
        result["NAME_INCOME_TYPE"]
        .fillna("Unknown")
    )

    result["default_rate"] *= 100

    return result

def employment_summary(df):
    """
    Overall employment statistics.

    Home Credit uses 365243 as a special value for
    unavailable employment information.
    """

    employment_days = (
        pd.to_numeric(
            df["DAYS_EMPLOYED"],
            errors="coerce"
        )
        .replace(365243, np.nan)
    )

    employment_years = (
        employment_days.abs() / 365.25
    )

    return {
        "average_employment_years": employment_years.mean(),
        "median_employment_years": employment_years.median(),
        "minimum_employment_years": employment_years.min(),
        "maximum_employment_years": employment_years.max(),
    }


def employment_group_distribution(df):
    """
    Customer distribution by employment duration.
    """

    employment_days = (
        pd.to_numeric(
            df["DAYS_EMPLOYED"],
            errors="coerce"
        )
        .replace(365243, np.nan)
    )

    employment_years = (
        employment_days.abs() / 365.25
    )

    groups = pd.cut(
        employment_years,
        bins=[
            0,
            2,
            5,
            10,
            20,
            float("inf")
        ],
        labels=[
            "<2 Years",
            "2-5 Years",
            "5-10 Years",
            "10-20 Years",
            "20+ Years"
        ],
        include_lowest=True
    )

    result = (
        groups
        .value_counts()
        .sort_index()
        .reset_index()
    )

    result.columns = [
        "EMPLOYMENT_GROUP",
        "customers"
    ]

    return result


def default_rate_by_employment_group(df):
    """
    Default rate by employment duration.
    """

    data = df.copy()

    employment_days = (
        pd.to_numeric(
            data["DAYS_EMPLOYED"],
            errors="coerce"
        )
        .replace(365243, np.nan)
    )

    data["EMPLOYMENT_YEARS"] = (
        employment_days.abs() / 365.25
    )

    data["EMPLOYMENT_GROUP"] = pd.cut(
        data["EMPLOYMENT_YEARS"],
        bins=[
            0,
            2,
            5,
            10,
            20,
            float("inf")
        ],
        labels=[
            "<2 Years",
            "2-5 Years",
            "5-10 Years",
            "10-20 Years",
            "20+ Years"
        ],
        include_lowest=True
    )

    result = (
        data.groupby(
            "EMPLOYMENT_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def employment_financial_summary(df):
    """
    Average income, credit and annuity by employment group.
    """

    data = df.copy()

    employment_days = (
        pd.to_numeric(
            data["DAYS_EMPLOYED"],
            errors="coerce"
        )
        .replace(365243, np.nan)
    )

    data["EMPLOYMENT_YEARS"] = (
        employment_days.abs() / 365.25
    )

    data["EMPLOYMENT_GROUP"] = pd.cut(
        data["EMPLOYMENT_YEARS"],
        bins=[
            0,
            2,
            5,
            10,
            20,
            float("inf")
        ],
        labels=[
            "<2 Years",
            "2-5 Years",
            "5-10 Years",
            "10-20 Years",
            "20+ Years"
        ],
        include_lowest=True
    )

    result = (
        data.groupby(
            "EMPLOYMENT_GROUP",
            observed=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    return result
def occupation_risk_summary(df):
    """
    Default rate by occupation.
    """

    result = (
        df.groupby(
            "OCCUPATION_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["OCCUPATION_TYPE"] = (
        result["OCCUPATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def organization_risk_summary(df):
    """
    Default rate by organization type.
    """

    result = (
        df.groupby(
            "ORGANIZATION_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["ORGANIZATION_TYPE"] = (
        result["ORGANIZATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )

def family_status_summary(df):
    """
    Customer distribution and default risk by family status.
    """

    result = (
        df.groupby(
            "NAME_FAMILY_STATUS",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["NAME_FAMILY_STATUS"] = (
        result["NAME_FAMILY_STATUS"]
        .astype("object")
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "customers",
        ascending=False
    )


def children_distribution(df):
    """
    Customer distribution by number of children.
    """

    result = (
        df["CNT_CHILDREN"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    result.columns = [
        "CNT_CHILDREN",
        "customers"
    ]

    return result


def family_size_distribution(df):
    """
    Customer distribution by family size.
    """

    result = (
        df["CNT_FAM_MEMBERS"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    result.columns = [
        "CNT_FAM_MEMBERS",
        "customers"
    ]

    return result


def default_rate_by_family_size(df):
    """
    Default rate by family size.
    """

    result = (
        df.groupby(
            "CNT_FAM_MEMBERS",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "CNT_FAM_MEMBERS"
    )


def family_financial_summary(df):
    """
    Average income, credit and annuity by family status.
    """

    result = (
        df.groupby(
            "NAME_FAMILY_STATUS",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["NAME_FAMILY_STATUS"] = (
        result["NAME_FAMILY_STATUS"]
        .astype("object")
        .fillna("Unknown")
    )

    return result


def children_risk_summary(df):
    """
    Default rate by number of children.
    """

    result = (
        df.groupby(
            "CNT_CHILDREN",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "CNT_CHILDREN"
    )
def housing_type_summary(df):
    """
    Customer distribution and default risk by housing type.
    """

    result = (
        df.groupby(
            "NAME_HOUSING_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["NAME_HOUSING_TYPE"] = (
        result["NAME_HOUSING_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "customers",
        ascending=False
    )


def car_ownership_summary(df):
    """
    Customer distribution and default risk by car ownership.
    """

    result = (
        df.groupby(
            "FLAG_OWN_CAR",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def realty_ownership_summary(df):
    """
    Customer distribution and default risk by realty ownership.
    """

    result = (
        df.groupby(
            "FLAG_OWN_REALTY",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def car_age_summary(df):
    """
    Statistics for customers who own a car.
    """

    car_age = pd.to_numeric(
        df["OWN_CAR_AGE"],
        errors="coerce"
    )

    return {
        "average_car_age": car_age.mean(),
        "median_car_age": car_age.median(),
        "minimum_car_age": car_age.min(),
        "maximum_car_age": car_age.max(),
        "car_age_known": car_age.notna().sum(),
    }


def car_age_risk_summary(df):
    """
    Default rate by car age group.
    """

    data = df.copy()

    data["CAR_AGE_GROUP"] = pd.cut(
        pd.to_numeric(
            data["OWN_CAR_AGE"],
            errors="coerce"
        ),
        bins=[
            0,
            3,
            5,
            10,
            15,
            20,
            float("inf")
        ],
        labels=[
            "0-3 Years",
            "3-5 Years",
            "5-10 Years",
            "10-15 Years",
            "15-20 Years",
            "20+ Years"
        ],
        include_lowest=True
    )

    result = (
        data.groupby(
            "CAR_AGE_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def housing_financial_summary(df):
    """
    Average income, credit and annuity by housing type.
    """

    result = (
        df.groupby(
            "NAME_HOUSING_TYPE",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["NAME_HOUSING_TYPE"] = (
        result["NAME_HOUSING_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    return result


def asset_ownership_summary(df):
    """
    Compare default risk across combinations of car and
    realty ownership.
    """

    data = df.copy()

    data["CAR_OWNER"] = (
        data["FLAG_OWN_CAR"]
        .map(
            {
                "Y": "Own Car",
                "N": "No Car"
            }
        )
        .fillna("Unknown")
    )

    data["REALTY_OWNER"] = (
        data["FLAG_OWN_REALTY"]
        .map(
            {
                "Y": "Own Realty",
                "N": "No Realty"
            }
        )
        .fillna("Unknown")
    )

    result = (
        data.groupby(
            [
                "CAR_OWNER",
                "REALTY_OWNER"
            ]
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result

def contract_type_summary(df):
    """
    Customer distribution and default risk by contract type.
    """

    result = (
        df.groupby(
            "NAME_CONTRACT_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["NAME_CONTRACT_TYPE"] = (
        result["NAME_CONTRACT_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "customers",
        ascending=False
    )


def contract_financial_summary(df):
    """
    Average income, credit and annuity by contract type.
    """

    result = (
        df.groupby(
            "NAME_CONTRACT_TYPE",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["NAME_CONTRACT_TYPE"] = (
        result["NAME_CONTRACT_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    return result


def contract_ratio_summary(df):
    """
    Credit-to-income ratio by contract type.
    """

    data = df.copy()

    data["CREDIT_INCOME_RATIO"] = (
        data["AMT_CREDIT"] /
        data["AMT_INCOME_TOTAL"]
    )

    result = (
        data.groupby(
            "NAME_CONTRACT_TYPE",
            dropna=False
        )["CREDIT_INCOME_RATIO"]
        .agg(
            average_ratio="mean",
            median_ratio="median",
            minimum_ratio="min",
            maximum_ratio="max"
        )
        .reset_index()
    )

    result["NAME_CONTRACT_TYPE"] = (
        result["NAME_CONTRACT_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    return result


def contract_income_risk(df):
    """
    Default risk by contract type and income group.
    """

    data = df.copy()

    if "INCOME_GROUP" not in data.columns:
        income_bins = [
            0,
            100000,
            150000,
            200000,
            float("inf")
        ]

        income_labels = [
            "Low Income",
            "Lower-Middle Income",
            "Upper-Middle Income",
            "High Income"
        ]

        data["INCOME_GROUP"] = pd.cut(
            data["AMT_INCOME_TOTAL"],
            bins=income_bins,
            labels=income_labels,
            include_lowest=True
        )

    result = (
        data.groupby(
            [
                "NAME_CONTRACT_TYPE",
                "INCOME_GROUP"
            ],
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result
def external_score_summary(df):
    """
    Summary statistics for external credit scores.
    """

    scores = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    result = []

    for score in scores:
        result.append(
            {
                "score": score,
                "average": df[score].mean(),
                "median": df[score].median(),
                "minimum": df[score].min(),
                "maximum": df[score].max(),
                "available": df[score].notna().sum(),
            }
        )

    return pd.DataFrame(result)


def external_score_default_summary(df):
    """
    Compare average external scores between default
    and non-default customers.
    """

    scores = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    result = []

    for score in scores:
        result.append(
            {
                "score": score,
                "default_average": df.loc[
                    df["TARGET"] == 1,
                    score
                ].mean(),
                "non_default_average": df.loc[
                    df["TARGET"] == 0,
                    score
                ].mean(),
            }
        )

    return pd.DataFrame(result)


def external_score_band_risk(df):
    """
    Default rate by external score bands.
    """

    data = df.copy()

    scores = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    results = []

    for score in scores:

        temp = data[
            [score, "TARGET"]
        ].dropna().copy()

        temp["SCORE_BAND"] = pd.cut(
            temp[score],
            bins=[
                0,
                0.2,
                0.4,
                0.6,
                0.8,
                1.0
            ],
            labels=[
                "0.0-0.2",
                "0.2-0.4",
                "0.4-0.6",
                "0.6-0.8",
                "0.8-1.0"
            ],
            include_lowest=True
        )

        grouped = (
            temp.groupby(
                "SCORE_BAND",
                observed=False
            )["TARGET"]
            .agg(
                customers="count",
                defaults="sum",
                default_rate="mean"
            )
            .reset_index()
        )

        grouped["default_rate"] *= 100
        grouped["score"] = score

        results.append(grouped)

    return pd.concat(
        results,
        ignore_index=True
    )


def combined_external_score(df):
    """
    Average available external scores for each customer.
    """

    data = df.copy()

    scores = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    data["COMBINED_EXTERNAL_SCORE"] = (
        data[scores].mean(axis=1)
    )

    return data


def combined_score_risk(df):
    """
    Default rate by combined external score band.
    """

    data = combined_external_score(df)

    data = data.dropna(
        subset=["COMBINED_EXTERNAL_SCORE"]
    )

    data["COMBINED_SCORE_BAND"] = pd.cut(
        data["COMBINED_EXTERNAL_SCORE"],
        bins=[
            0,
            0.2,
            0.4,
            0.6,
            0.8,
            1.0
        ],
        labels=[
            "0.0-0.2",
            "0.2-0.4",
            "0.4-0.6",
            "0.6-0.8",
            "0.8-1.0"
        ],
        include_lowest=True
    )

    result = (
        data.groupby(
            "COMBINED_SCORE_BAND",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result

def region_rating_summary(df):
    """
    Customer distribution and default risk by region rating.
    """

    result = (
        df.groupby(
            "REGION_RATING_CLIENT",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["REGION_RATING_CLIENT"] = (
        result["REGION_RATING_CLIENT"]
        .astype(object)
    )

    result.loc[
        result["REGION_RATING_CLIENT"].isna(),
        "REGION_RATING_CLIENT"
    ] = "Unknown"

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "REGION_RATING_CLIENT"
    )


def region_city_rating_summary(df):
    """
    Default risk by region rating and region rating within city.
    """

    result = (
        df.groupby(
            [
                "REGION_RATING_CLIENT",
                "REGION_RATING_CLIENT_W_CITY"
            ],
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def population_region_summary(df):
    """
    Summary of relative population density by region.
    """

    return {
        "average_population_relative":
            df["REGION_POPULATION_RELATIVE"].mean(),

        "median_population_relative":
            df["REGION_POPULATION_RELATIVE"].median(),

        "minimum_population_relative":
            df["REGION_POPULATION_RELATIVE"].min(),

        "maximum_population_relative":
            df["REGION_POPULATION_RELATIVE"].max(),
    }


def population_density_risk(df):
    """
    Default risk by relative population density bands.
    """

    data = df.copy()

    data["POPULATION_GROUP"] = pd.qcut(
        data["REGION_POPULATION_RELATIVE"],
        q=5,
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Very High"
        ],
        duplicates="drop"
    )

    result = (
        data.groupby(
            "POPULATION_GROUP",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def region_financial_summary(df):
    """
    Average income, credit and annuity by region rating.
    """

    result = (
        df.groupby(
            "REGION_RATING_CLIENT",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["REGION_RATING_CLIENT"] = (
        result["REGION_RATING_CLIENT"]
        .astype(object)
    )

    result.loc[
        result["REGION_RATING_CLIENT"].isna(),
        "REGION_RATING_CLIENT"
    ] = "Unknown"
    

    return result


def region_risk_summary(df):
    """
    Combined regional risk summary using client rating
    and city rating.
    """

    result = (
        df.groupby(
            [
                "REGION_RATING_CLIENT",
                "REGION_RATING_CLIENT_W_CITY"
            ],
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )

def occupation_risk_summary(df):
    """
    Customer distribution and default risk by occupation.
    """

    result = (
        df.groupby(
            "OCCUPATION_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["OCCUPATION_TYPE"] = (
        result["OCCUPATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def organization_risk_summary(df):
    """
    Customer distribution and default risk by organization type.
    """

    result = (
        df.groupby(
            "ORGANIZATION_TYPE",
            dropna=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["ORGANIZATION_TYPE"] = (
        result["ORGANIZATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["non_defaults"] = (
        result["customers"] -
        result["defaults"]
    )

    result["default_rate"] *= 100

    return result.sort_values(
        "default_rate",
        ascending=False
    )


def occupation_financial_summary(df):
    """
    Average income, credit and annuity by occupation.
    """

    result = (
        df.groupby(
            "OCCUPATION_TYPE",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["OCCUPATION_TYPE"] = (
        result["OCCUPATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    return result


def organization_financial_summary(df):
    """
    Average income, credit and annuity by organization type.
    """

    result = (
        df.groupby(
            "ORGANIZATION_TYPE",
            dropna=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    result["ORGANIZATION_TYPE"] = (
        result["ORGANIZATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    return result


def occupation_income_risk(df):
    """
    Default risk by occupation and income group.
    """

    data = df.copy()

    if "INCOME_GROUP" not in data.columns:

        income_bins = [
            0,
            100000,
            150000,
            200000,
            float("inf")
        ]

        income_labels = [
            "Low Income",
            "Lower-Middle Income",
            "Upper-Middle Income",
            "High Income"
        ]

        data["INCOME_GROUP"] = pd.cut(
            data["AMT_INCOME_TOTAL"],
            bins=income_bins,
            labels=income_labels,
            include_lowest=True
        )

    result = (
        data.groupby(
            [
                "OCCUPATION_TYPE",
                "INCOME_GROUP"
            ],
            dropna=False,
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["OCCUPATION_TYPE"] = (
        result["OCCUPATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["default_rate"] *= 100

    return result


def organization_income_risk(df):
    """
    Default risk by organization type and income group.
    """

    data = df.copy()

    if "INCOME_GROUP" not in data.columns:

        income_bins = [
            0,
            100000,
            150000,
            200000,
            float("inf")
        ]

        income_labels = [
            "Low Income",
            "Lower-Middle Income",
            "Upper-Middle Income",
            "High Income"
        ]

        data["INCOME_GROUP"] = pd.cut(
            data["AMT_INCOME_TOTAL"],
            bins=income_bins,
            labels=income_labels,
            include_lowest=True
        )

    result = (
        data.groupby(
            [
                "ORGANIZATION_TYPE",
                "INCOME_GROUP"
            ],
            dropna=False,
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["ORGANIZATION_TYPE"] = (
        result["ORGANIZATION_TYPE"]
        .astype("object")
        .fillna("Unknown")
    )

    result["default_rate"] *= 100

    return result

def create_risk_segments(df):
    """
    Create combined customer risk segments using
    external score, credit burden, annuity burden,
    income group and region rating.
    """

    data = df.copy()

    # --------------------------------------------------------
    # Combined external score
    # --------------------------------------------------------

    external_scores = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    data["COMBINED_EXTERNAL_SCORE"] = (
        data[external_scores].mean(axis=1)
    )

    # --------------------------------------------------------
    # External score group
    # --------------------------------------------------------

    data["EXTERNAL_SCORE_GROUP"] = pd.cut(
        data["COMBINED_EXTERNAL_SCORE"],
        bins=[
            0,
            0.4,
            0.6,
            0.8,
            1.0
        ],
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High"
        ],
        include_lowest=True
    )

    # --------------------------------------------------------
    # Credit / income ratio
    # --------------------------------------------------------

    data["CREDIT_INCOME_RATIO"] = (
        data["AMT_CREDIT"] /
        data["AMT_INCOME_TOTAL"]
    )

    data["CREDIT_BURDEN_GROUP"] = pd.cut(
        data["CREDIT_INCOME_RATIO"],
        bins=[
            0,
            2,
            4,
            6,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ],
        include_lowest=True
    )

    # --------------------------------------------------------
    # Annuity / income ratio
    # --------------------------------------------------------

    data["ANNUITY_INCOME_RATIO"] = (
        data["AMT_ANNUITY"] /
        data["AMT_INCOME_TOTAL"]
    )

    data["ANNUITY_BURDEN_GROUP"] = pd.cut(
        data["ANNUITY_INCOME_RATIO"],
        bins=[
            0,
            0.1,
            0.2,
            0.3,
            float("inf")
        ],
        labels=[
            "<10%",
            "10%-20%",
            "20%-30%",
            "30%+"
        ],
        include_lowest=True
    )

    # --------------------------------------------------------
    # Income group
    # --------------------------------------------------------

    if "INCOME_GROUP" not in data.columns:

        data["INCOME_GROUP"] = pd.cut(
            data["AMT_INCOME_TOTAL"],
            bins=[
                0,
                100000,
                150000,
                200000,
                float("inf")
            ],
            labels=[
                "Low Income",
                "Lower-Middle Income",
                "Upper-Middle Income",
                "High Income"
            ],
            include_lowest=True
        )

    # --------------------------------------------------------
    # Region risk
    # --------------------------------------------------------

    data["REGION_RISK_GROUP"] = data[
        "REGION_RATING_CLIENT"
    ].map(
        {
            1: "Low Regional Risk",
            2: "Medium Regional Risk",
            3: "High Regional Risk"
        }
    )

    # --------------------------------------------------------
    # Final combined risk score
    # --------------------------------------------------------

    external_risk = (
        data["EXTERNAL_SCORE_GROUP"]
        .map(
            {
                "Very Low": 3,
                "Low": 2,
                "Medium": 1,
                "High": 0
            }
        )
        .astype(float)
        .fillna(1.0)
    )

    credit_risk = (
        data["CREDIT_BURDEN_GROUP"]
        .map(
            {
                "Low": 0,
                "Moderate": 1,
                "High": 2,
                "Very High": 3
            }
        )
        .astype(float)
        .fillna(1.0)
    )

    annuity_risk = (
        data["ANNUITY_BURDEN_GROUP"]
        .map(
            {
                "<10%": 0,
                "10%-20%": 1,
                "20%-30%": 2,
                "30%+": 3
            }
        )
        .astype(float)
        .fillna(1.0)
    )

    region_risk = (
        data["REGION_RATING_CLIENT"]
        .map(
            {
                1: 0,
                2: 1,
                3: 2
            }
        )
        .astype(float)
        .fillna(1.0)
    )

    data["RISK_SCORE"] = (
        external_risk
        + credit_risk
        + annuity_risk
        + region_risk
    )

    # --------------------------------------------------------
    # Risk category
    # --------------------------------------------------------

    data["RISK_CATEGORY"] = pd.cut(
        data["RISK_SCORE"],
        bins=[
            -1,
            2,
            5,
            8,
            float("inf")
        ],
        labels=[
            "Low Risk",
            "Moderate Risk",
            "High Risk",
            "Very High Risk"
        ]
    )

    return data

def risk_segment_summary(df):
    """
    Customer count and default rate by combined risk category.
    """

    data = create_risk_segments(df)

    result = (
        data.groupby(
            "RISK_CATEGORY",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def risk_segment_income_summary(df):
    """
    Risk category by income group.
    """

    data = create_risk_segments(df)

    result = (
        data.groupby(
            [
                "RISK_CATEGORY",
                "INCOME_GROUP"
            ],
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def risk_segment_contract_summary(df):
    """
    Risk category by contract type.
    """

    data = create_risk_segments(df)

    result = (
        data.groupby(
            [
                "RISK_CATEGORY",
                "NAME_CONTRACT_TYPE"
            ],
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    return result


def high_risk_customer_summary(df):
    """
    Summary of customers classified as High or Very High Risk.
    """

    data = create_risk_segments(df)

    high_risk = data[
        data["RISK_CATEGORY"].isin(
            [
                "High Risk",
                "Very High Risk"
            ]
        )
    ]

    return {
        "customers": len(high_risk),
        "defaults": int(high_risk["TARGET"].sum()),
        "default_rate": (
            high_risk["TARGET"].mean() * 100
            if len(high_risk) > 0
            else 0
        ),
        "average_income": high_risk[
            "AMT_INCOME_TOTAL"
        ].mean(),
        "average_credit": high_risk[
            "AMT_CREDIT"
        ].mean(),
        "average_external_score": high_risk[
            "COMBINED_EXTERNAL_SCORE"
        ].mean(),
    }
def portfolio_summary(df):
    """
    Overall portfolio-level financial and credit metrics.
    """

    total_customers = len(df)

    total_defaults = int(
        df["TARGET"].sum()
    )

    default_rate = (
        df["TARGET"].mean() * 100
        if total_customers > 0
        else 0
    )

    return {
        "total_customers": total_customers,
        "total_defaults": total_defaults,
        "default_rate": default_rate,
        "total_income": df["AMT_INCOME_TOTAL"].sum(),
        "total_credit": df["AMT_CREDIT"].sum(),
        "total_annuity": df["AMT_ANNUITY"].sum(),
        "average_income": df["AMT_INCOME_TOTAL"].mean(),
        "average_credit": df["AMT_CREDIT"].mean(),
        "average_annuity": df["AMT_ANNUITY"].mean(),
    }


def portfolio_risk_distribution(df):
    """
    Overall portfolio distribution by combined risk category.
    """

    data = create_risk_segments(df)

    result = (
        data.groupby(
            "RISK_CATEGORY",
            observed=False
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    result["portfolio_share"] = (
        result["customers"] /
        result["customers"].sum() *
        100
    )

    return result


def portfolio_contract_summary(df):
    """
    Portfolio distribution and risk by contract type.
    """

    result = (
        df.groupby(
            "NAME_CONTRACT_TYPE"
        )["TARGET"]
        .agg(
            customers="count",
            defaults="sum",
            default_rate="mean"
        )
        .reset_index()
    )

    result["default_rate"] *= 100

    result["portfolio_share"] = (
        result["customers"] /
        result["customers"].sum() *
        100
    )

    return result


def portfolio_credit_exposure(df):
    """
    Credit exposure summary by contract type.
    """

    result = (
        df.groupby(
            "NAME_CONTRACT_TYPE"
        )[
            [
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .agg(
            total_credit=("AMT_CREDIT", "sum"),
            average_credit=("AMT_CREDIT", "mean"),
            total_annuity=("AMT_ANNUITY", "sum"),
            average_annuity=("AMT_ANNUITY", "mean")
        )
        .reset_index()
    )

    return result


def portfolio_income_credit_summary(df):
    """
    Income and credit summary by income group.
    """

    data = df.copy()

    if "INCOME_GROUP" not in data.columns:

        data["INCOME_GROUP"] = pd.cut(
            data["AMT_INCOME_TOTAL"],
            bins=[
                0,
                100000,
                150000,
                200000,
                float("inf")
            ],
            labels=[
                "Low Income",
                "Lower-Middle Income",
                "Upper-Middle Income",
                "High Income"
            ],
            include_lowest=True
        )

    result = (
        data.groupby(
            "INCOME_GROUP",
            observed=False
        )[
            [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]
        ]
        .mean()
        .reset_index()
    )

    return result


def portfolio_risk_metrics(df):
    """
    Key portfolio risk metrics derived from combined risk segmentation.
    """

    data = create_risk_segments(df)

    high_risk = data[
        data["RISK_CATEGORY"].isin(
            [
                "High Risk",
                "Very High Risk"
            ]
        )
    ]

    very_high_risk = data[
        data["RISK_CATEGORY"] == "Very High Risk"
    ]

    return {
        "high_risk_customers": len(high_risk),

        "high_risk_share": (
            len(high_risk) /
            len(data) *
            100
            if len(data) > 0
            else 0
        ),

        "high_risk_defaults": int(
            high_risk["TARGET"].sum()
        ),

        "high_risk_default_rate": (
            high_risk["TARGET"].mean() * 100
            if len(high_risk) > 0
            else 0
        ),

        "very_high_risk_customers": len(
            very_high_risk
        ),

        "very_high_risk_share": (
            len(very_high_risk) /
            len(data) *
            100
            if len(data) > 0
            else 0
        ),

        "very_high_risk_default_rate": (
            very_high_risk["TARGET"].mean() * 100
            if len(very_high_risk) > 0
            else 0
        ),
    }