import pandas as pd

DATA_PATH = "data/application_train.csv"


def profile_data():
    print("=" * 60)
    print("HOME CREDIT DATASET PROFILE")
    print("=" * 60)

    total_rows = 0
    target_0 = 0
    target_1 = 0

    # Store SK_ID_CURR values to check duplicates across chunks
    all_ids = set()
    duplicate_ids = 0

    missing_counts = None

    for chunk in pd.read_csv(DATA_PATH, chunksize=50000):

        total_rows += len(chunk)

        # TARGET distribution
        target_0 += (chunk["TARGET"] == 0).sum()
        target_1 += (chunk["TARGET"] == 1).sum()

        # Missing values
        chunk_missing = chunk.isna().sum()

        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts += chunk_missing

        # Check duplicate SK_ID_CURR across the entire dataset
        for customer_id in chunk["SK_ID_CURR"]:
            if customer_id in all_ids:
                duplicate_ids += 1
            else:
                all_ids.add(customer_id)

    print(f"\nTotal Rows      : {total_rows:,}")
    print(f"Total Columns   : 122")

    print("\nTARGET DISTRIBUTION")
    print("-" * 40)

    print(f"TARGET = 0     : {target_0:,}")
    print(f"TARGET = 1     : {target_1:,}")

    default_rate = (target_1 / total_rows) * 100

    print(f"Default Rate    : {default_rate:.2f}%")

    print("\nTOP 15 MISSING COLUMNS")
    print("-" * 40)

    missing_percentage = (
        missing_counts / total_rows * 100
    ).sort_values(ascending=False)

    print(missing_percentage.head(15))

    print("\nDuplicate SK_ID_CURR:", duplicate_ids)

    print("\n" + "=" * 60)
    print("PROFILE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    profile_data()