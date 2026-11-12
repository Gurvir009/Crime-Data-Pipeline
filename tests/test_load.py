from src.extract import extract_data
from src.validate import validate_data
from src.transform import transform_data
from src.load import load_data

# Step 1: Extract
df = extract_data.fn()
print("Records extracted:", len(df))

# Step 2: Validate
validated_df = validate_data.fn(df)
print("Records validated:", len(validated_df))

# Step 3: Transform
transformed_df = transform_data.fn(validated_df)
print("Records transformed:", len(transformed_df))

# Step 4: Load into PostgreSQL
records_loaded = load_data.fn(transformed_df)
print("Records processed for loading:", records_loaded)

print("ETL pipeline completed successfully!")
