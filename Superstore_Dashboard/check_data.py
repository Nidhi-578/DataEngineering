# import pandas as pd

# file_path = "data/sample_-_superstore.csv"

# df = pd.read_csv(file_path)

# print("Number of rows:", len(df))
# print("Number of columns:", len(df.columns))

# print("\nColumn names:")
# print(df.columns.tolist())

# print("\nFirst 5 rows:")
# print(df.head())

# print("\nData types:")
# print(df.dtypes)

# print("\nMissing values:")
# print(df.isnull().sum())

from utils.data_loader import load_data


file_path = "data/sample_-_superstore.csv"

df = load_data(file_path)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nDate columns:")
print(df[["Order Date", "Ship Date"]].dtypes)

print("\nShipping Days:")
print(df["Shipping Days"].head())

print("\nFirst row:")
print(df.iloc[0])