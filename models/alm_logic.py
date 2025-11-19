import pandas as pd
from config import ANALYSIS_DATE, BUCKET_LABELS, BUCKET_THRESHOLDS

def prepare_data(data_df):
    """Prepares raw data by calculating day counts and signed amounts."""
    if data_df.empty:
        print("WARNING: Input data is empty.")
        return data_df

    df = data_df.copy()
    analysis_date = pd.to_datetime(ANALYSIS_DATE)

    # Calculate days difference
    df['days_to_maturity'] = (df['maturity_date'] - analysis_date).dt.days
    df['days_to_repricing'] = (df['repricing_date'] - analysis_date).dt.days

    # Set Assets as positive and Liabilities as negative
    df['amount_signed'] = df.apply(
        lambda row: row['amount'] if row['type'] == 'Asset' else -row['amount'],
        axis=1
    )
    return df

def bucket_cashflows(data_df, date_column_name):
    """Assigns rows to time buckets and pivots them into Assets/Liabilities columns."""
    df = data_df.copy()
    days_col = f'days_to_{date_column_name.lower().replace("_date", "")}'
    
    bins = [-1] + BUCKET_THRESHOLDS
    
    df['bucket'] = pd.cut(
        df[days_col],
        bins=bins,
        labels=BUCKET_LABELS,
        right=True,
        include_lowest=True
    )
    
    df['bucket'] = df['bucket'].cat.add_categories('Non-Sensitive').fillna('Non-Sensitive')
    
    # Aggregate (Sum)
    bucketed_data = df.groupby(['bucket', 'type'])['amount'].sum().unstack(fill_value=0)
    
    all_buckets = BUCKET_LABELS + ['Non-Sensitive']
    bucketed_data = bucketed_data.reindex(all_buckets, fill_value=0)
    
    if 'Asset' not in bucketed_data.columns: bucketed_data['Asset'] = 0
    if 'Liability' not in bucketed_data.columns: bucketed_data['Liability'] = 0
        
    bucketed_data.rename(columns={'Asset': 'Assets', 'Liability': 'Liabilities'}, inplace=True)
    
    return bucketed_data[['Assets', 'Liabilities']]

def calculate_gap(data_df, date_column_name):
    """Calculates Static and Cumulative gaps."""
    bucketed_df = bucket_cashflows(data_df, date_column_name)
    bucketed_df['Static Gap'] = bucketed_df['Assets'] - bucketed_df['Liabilities']
    
    time_buckets = bucketed_df.loc[BUCKET_LABELS]
    bucketed_df['Cumulative Gap'] = time_buckets['Static Gap'].cumsum().reindex(bucketed_df.index).fillna(0)

    return bucketed_df

def get_liquidity_gap(data_df):
    if 'days_to_maturity' not in data_df.columns:
        data_df = prepare_data(data_df)
    return calculate_gap(data_df, 'maturity_date')

def get_repricing_gap(data_df):
    if 'days_to_repricing' not in data_df.columns:
        data_df = prepare_data(data_df)
    return calculate_gap(data_df, 'repricing_date')

# --- NEW FUNCTION ADDED HERE ---
def get_detailed_view(data_df):
    """
    Returns the raw data with ALL calculations columns added (Days, Buckets).
    It does NOT aggregate/sum the data.
    """
    # 1. Get basic calcs (days remaining)
    if 'days_to_maturity' not in data_df.columns:
        df = prepare_data(data_df)
    else:
        df = data_df.copy()
        
    bins = [-1] + BUCKET_THRESHOLDS
    
    # 2. Assign Liquidity Bucket
    df['Liquidity_Bucket'] = pd.cut(
        df['days_to_maturity'], bins=bins, labels=BUCKET_LABELS, right=True, include_lowest=True
    )
    df['Liquidity_Bucket'] = df['Liquidity_Bucket'].cat.add_categories('Non-Sensitive').fillna('Non-Sensitive')

    # 3. Assign Repricing Bucket
    df['Repricing_Bucket'] = pd.cut(
        df['days_to_repricing'], bins=bins, labels=BUCKET_LABELS, right=True, include_lowest=True
    )
    df['Repricing_Bucket'] = df['Repricing_Bucket'].cat.add_categories('Non-Sensitive').fillna('Non-Sensitive')
    
    return df