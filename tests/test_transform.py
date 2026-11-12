from src.extract import extract_data
from src.validate import validate_data
from src.transform import transform_data

# Extract the incident data
df = extract_data.fn()

# Validate the extracted data
validated_df = validate_data.fn(df)

# Transform the validated data
transformed_df = transform_data.fn(validated_df)

# Display record counts
print("Records after extraction:", len(df))
print("Records after validation:", len(validated_df))
print("Records after transformation:", len(transformed_df))

# Display column names
print("\nTransformed columns:")
print(transformed_df.columns.tolist())

# Display the first five records
print("\nFirst five transformed records:")
print(transformed_df.head())

# Check that all expected time columns were created
time_columns = ["year", "month", "day", "hour", "minute", "second"]

for column in time_columns:
    assert column in transformed_df.columns

print("\nAll time columns were created successfully.")