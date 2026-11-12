import pandas as pd
from prefect import task

def check_columns(df):
    # Columns needed by the next pipeline stages
    required_columns = [
        "date_time", "id", "type", "subtype",
        "location", "last_updated", "description"
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

def check_ids(df):
    # Convert incident IDs to numeric values
    df["id"] = pd.to_numeric(df["id"], errors="coerce")

    # Remove records without a valid ID
    df = df.dropna(subset=["id"]).copy()

    # Incident IDs must be whole numbers
    if (df["id"] % 1 != 0).any():
        raise ValueError("Some incident IDs are not whole numbers")

    # Use integer IDs
    df["id"] = df["id"].astype("int64")

    return df

def check_dates(df):
    # Convert date/time strings into datetime values
    df["date_time"] = pd.to_datetime(
        df["date_time"], errors="coerce"
    )

    if df["date_time"].isna().any():
        raise ValueError("Some records contain invalid date_time values")

    return df

def check_required_values(df):
    # These fields must be present
    required_fields = ["date_time", "type", "location"]

    if df[required_fields].isna().any().any():
        raise ValueError("Required fields contain missing values")

    # Check that type and location are not blank
    for column in ["type", "location"]:
        blank = df[column].astype("string").str.strip().eq("")

        if blank.any():
            raise ValueError(f"Blank values found in {column}")

def remove_duplicate_ids(df):
    # Keep the first record for each incident ID
    return df.drop_duplicates(subset=["id"], keep="first").copy()

@task
def validate_data(df):
    # Avoid changing the original extracted DataFrame
    df = df.copy()

    if df.empty:
        raise ValueError("No incident records were extracted")

    check_columns(df)

    df = check_ids(df)

    if df.empty:
        raise ValueError("No records with valid incident IDs remain")

    df = check_dates(df)
    check_required_values(df)

    # Keep only one record per incident ID
    df = remove_duplicate_ids(df)

    print(f"Validation completed: {len(df)} records are valid.")

    return df