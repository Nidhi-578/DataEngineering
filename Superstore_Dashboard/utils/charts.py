import plotly.express as px


def sales_by_region(df):
    """Sales by Region."""

    data = (
        df.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        data,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    return fig


def sales_by_category(df):
    """Sales by Category."""

    data = (
        df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        data,
        x="Category",
        y="Sales",
        title="Sales by Category"
    )

    return fig


def profit_by_category(df):
    """Profit by Category."""

    data = (
        df.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig = px.bar(
        data,
        x="Category",
        y="Profit",
        title="Profit by Category"
    )

    return fig


def monthly_sales_profit(df):
    """Monthly Sales and Profit trend."""

    monthly = (
        df.set_index("Order Date")
        .resample("MS")[["Sales", "Profit"]]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Order Date",
        y=["Sales", "Profit"],
        markers=True,
        title="Monthly Sales & Profit Trend"
    )

    return fig


def top_subcategories(df, n=10):
    """Top N sub-categories by Sales."""

    data = (
        df.groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(n)
    )

    fig = px.bar(
        data,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title=f"Top {n} Sub-Categories by Sales"
    )

    return fig


def top_products(df, n=10):
    """Top N products by Sales."""

    data = (
        df.groupby("Product Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(n)
    )

    fig = px.bar(
        data,
        x="Sales",
        y="Product Name",
        orientation="h",
        title=f"Top {n} Products by Sales"
    )

    return fig