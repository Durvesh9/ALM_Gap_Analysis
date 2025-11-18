import datetime

# --- Database Configuration (PostgreSQL using psycopg2 dialect) ---
DB_CONFIG = {
    'DIALECT': 'postgresql+psycopg2',
    'HOST': 'localhost',
    'DATABASE': 'alm_db',
    'USER': 'postgres',
    'PASSWORD': 'password',  # *** UPDATE THIS ***
    'PORT': 5432
}

def get_db_url():
    """Constructs the connection URL for SQLAlchemy with psycopg2."""
    return (
        f"{DB_CONFIG['DIALECT']}://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@"
        f"{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['DATABASE']}"
    )

# --- ALM Analysis Configuration ---
ALM_BUCKETS = {
    'Overnight': 1,
    '1 Week': 7,
    '1 Month': 30,
    '3 Months': 90,
    '6 Months': 180,
    '1 Year': 365,
    '3 Years': 1095,
    '5 Years': 1825,
    'Over 5Y': 10000 
}
BUCKET_LABELS = list(ALM_BUCKETS.keys())
BUCKET_THRESHOLDS = list(ALM_BUCKETS.values())

ANALYSIS_DATE = datetime.date(2023, 11, 21)

# --- Scenario Analysis ---
RATE_SHOCKS = {
    'Base': 0.00,
    '+100bp': 0.01,
    '-100bp': -0.01,
}

# File Paths
CSV_FILE_PATH = 'data/alm_data.csv'
SCHEMA_FILE_PATH = 'data/schema.sql'
OUTPUT_DIR = 'output'
OUTPUT_FILE_PATH = f'{OUTPUT_DIR}/alm_gap_report.xlsx'
TABLE_NAME = 'alm_cashflows'