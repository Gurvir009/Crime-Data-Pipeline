from prefect import flow
from src.extract import extract_data
from src.validate import validate_data
from src.transform import transform_data
from src.load import load_data

@flow(name="cpd_incident_etl", log_prints=True)
def run_pipeline():

    print("Extracting data...")
    extracted_df = extract_data()
    print(f"Extracted {len(extracted_df)} records.")

    print("Performing data quality checks...")
    validated_df = validate_data(extracted_df)
    print("Data quality checks completed!")

    print("Performing data transformations...")
    transformed_df = transform_data(validated_df)
    print("Data transformations completed!")

    print("Importing data into PostgreSQL...")
    records_loaded = load_data(transformed_df)
    print(f"Processed {records_loaded} records for loading.")

    print("Crime data pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline.serve(
        name="cpd-incident-deployment",
        cron="5 15 * * *"
    )