import os
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv
from prefect import task

@task(retries=3, retry_delay_seconds=10)
def extract_data():
    # Load environment variables from the .env file
    load_dotenv()

    app_token = os.getenv("SOCRATA_APP_TOKEN")

    if not app_token:
        raise ValueError("SOCRATA_APP_TOKEN is missing from the .env file.")

    # Connect to the Cambridge open-data API
    client = Socrata(
        "data.cambridgema.gov",
        app_token,
        timeout=30
    )

    try:
        dataset_id = "3gki-wyrb"

        # Fetch all available incident records
        records = client.get_all(dataset_id)

        # Convert the records into a Pandas DataFrame
        df = pd.DataFrame.from_records(records)

        print(f"Extraction completed: {len(df)} records fetched.")

        return df

    finally:
        # Close the API connection
        client.close()