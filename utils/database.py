import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import get_db_url, TABLE_NAME, SCHEMA_FILE_PATH, CSV_FILE_PATH

def get_db_engine():                                    #Creates and returns the SQLAlchemy engine
    try:
        engine = create_engine(get_db_url())
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("INFO: Successfully connected to the PostgreSQL database using SQLAlchemy/psycopg2.")
        return engine
    except SQLAlchemyError as e:
        print(f"ERROR: Could not connect to the database. Check config.py and PostgreSQL setup. Details: {e}")
        return None

def setup_database(engine):
    #Creates the table structure defined in schema.sql.
    print("--- 1. Database Setup: Creating tables ---")
    if engine is None: return

    try:
        with open(SCHEMA_FILE_PATH, 'r') as f:
            schema_sql = f.read()
        
        with engine.connect() as connection:
            connection.execute(text(schema_sql))
            connection.commit()
        print(f"INFO: Table '{TABLE_NAME}' created/ensured in database.")
    except Exception as e:
        print(f"ERROR creating table: {e}")

def load_data_to_db(engine):
    """Loads data from CSV into the database table."""
    print("--- 2. Data Loading: Loading CSV into DB ---")
    if engine is None: return

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
        print(f"INFO: Successfully loaded {len(df)} records into '{TABLE_NAME}'.")
    except FileNotFoundError:
        print(f"ERROR: CSV file not found at {CSV_FILE_PATH}")
    except Exception as e:
        print(f"ERROR loading data: {e}")

def fetch_data_from_db(engine):
    """Fetches all data from the ALM cashflows table as a pandas DataFrame."""
    print("--- 3. Data Fetching: Reading from DB ---")
    if engine is None: return pd.DataFrame()

    query = f"SELECT * FROM {TABLE_NAME}"
    try:
        df = pd.read_sql(query, engine)
        
        # Ensure date columns are datetime objects
        df['maturity_date'] = pd.to_datetime(df['maturity_date'])
        df['repricing_date'] = pd.to_datetime(df['repricing_date'])

        print(f"INFO: Successfully fetched {len(df)} records for analysis.")
        return df
    except Exception as e:
        print(f"ERROR fetching data: {e}")
        return pd.DataFrame()