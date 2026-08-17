import pandas as pd


def load_data(file_path):
    """
    Load and prepare the Superstore dataset.
    """

    df = pd.read_csv(file_path)

    # Convert date columns
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        dayfirst=True
    )

    # Calculate shipping duration
    df["Shipping Days"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    return df