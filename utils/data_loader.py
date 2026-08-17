import pandas as pd

DATA_PATH = "data/application_train.csv"


def load_data(nrows=None):
    """
    Load Home Credit application data.

    Parameters:
        nrows (int, optional): Number of rows to load.
                             If None, loads the complete dataset.

    Returns:
        pandas.DataFrame
    """

    return pd.read_csv(
        DATA_PATH,
        nrows=nrows
    )


def load_data_in_chunks(chunksize=50000):
    """
    Load the dataset in chunks to reduce memory usage.

    Parameters:
        chunksize (int): Number of rows per chunk.

    Returns:
        pandas TextFileReader
    """

    return pd.read_csv(
        DATA_PATH,
        chunksize=chunksize
    )