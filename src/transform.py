import pandas as pd
from prefect import task

@task
def transform_data(df):
    # Make a separate copy of the validated data
    transformed_df = df.copy()

    # Ensure date_time is stored as datetime
    transformed_df["date_time"] = pd.to_datetime(
        transformed_df["date_time"]
    )

    # Create separate columns for analysis
    date_time = transformed_df["date_time"]

    transformed_df["year"] = date_time.dt.year
    transformed_df["month"] = date_time.dt.month
    transformed_df["day"] = date_time.dt.day
    transformed_df["hour"] = date_time.dt.hour
    transformed_df["minute"] = date_time.dt.minute
    transformed_df["second"] = date_time.dt.second
    transformed_df["weekday"] = date_time.dt.day_name()

    print(
        f"Transformation completed: {len(transformed_df)} records processed."
    )

    return transformed_df