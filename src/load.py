import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from prefect import task

load_dotenv()

@task
def load_data(df):
    if df.empty:
        raise ValueError("No records to load.")
    df = df.copy()
    
    # Connect to PostgreSQL using .env settings
    connection_url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB")
    )
    engine = create_engine(connection_url)

    # Create table if it does not exist
    create_table = """
    CREATE TABLE IF NOT EXISTS cpd_incidents (
        date_time TIMESTAMP,
        id BIGINT PRIMARY KEY,
        type TEXT,
        subtype TEXT,
        location TEXT,
        description TEXT,
        last_updated TEXT,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        weekday TEXT,
        hour INTEGER,
        minute INTEGER,
        second INTEGER
    );
    """
    # Add weekday column to existing tables if missing
    add_weekday_column = """
    ALTER TABLE cpd_incidents
    ADD COLUMN IF NOT EXISTS weekday TEXT;
    """
    # Insert new records or update existing records
    upsert = """
    INSERT INTO cpd_incidents
    (date_time, id, type, subtype, location, description,
     last_updated, year, month, day, weekday, hour, minute, second)
    VALUES
    (:date_time, :id, :type, :subtype, :location, :description,
     :last_updated, :year, :month, :day, :weekday, :hour, :minute, :second)

    ON CONFLICT (id) DO UPDATE SET
        date_time = EXCLUDED.date_time,
        type = EXCLUDED.type,
        subtype = EXCLUDED.subtype,
        location = EXCLUDED.location,
        description = EXCLUDED.description,
        last_updated = EXCLUDED.last_updated,
        year = EXCLUDED.year,
        month = EXCLUDED.month,
        day = EXCLUDED.day,
        weekday = EXCLUDED.weekday,
        hour = EXCLUDED.hour,
        minute = EXCLUDED.minute,
        second = EXCLUDED.second;
    """
    try:
        # Handle missing values
        df = df.astype(object).where(pd.notna(df), None)
        records = df.to_dict(orient="records")
        with engine.begin() as connection:
            connection.execute(text(create_table))
            connection.execute(text(add_weekday_column))
            connection.execute(text(upsert), records)

        print(f"Loaded {len(records)} records into PostgreSQL.")
        return len(records)
    
    finally:
        engine.dispose()