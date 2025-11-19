import pandas as pd
from config import ANALYSIS_DATE, BUCKET_LABELS, BUCKET_THRESHOLDS

class ALMGapAnalyzer:
    def __init__(self, data_df):
        self.data_df = data_df.copy()
        if self.data_df.empty:
            print("WARNING: Analyzer initialized with empty data.")
        
        self._prepare_data()

    def _prepare_data(self):
        """Calculates days remaining to maturity/repricing and sets signed amounts."""
        analysis_date = pd.to_datetime(ANALYSIS_DATE)
        
        # Calculate days difference
        self.data_df['days_to_maturity'] = (self.data_df['maturity_date'] - analysis_date).dt.days
        self.data_df['days_to_repricing'] = (self.data_df['repricing_date'] - analysis_date).dt.days
        
        # Set Assets as positive and Liabilities as negative for easy math
        self.data_df['amount_signed'] = self.data_df.apply(
            lambda row: row['amount'] if row['type'] == 'Asset' else -row['amount'], 
            axis=1
        )

    def _bucket_cashflows(self, date_column_name):
        """Assigns rows to time buckets and pivots them into Assets/Liabilities columns."""
        df = self.data_df.copy()
        days_col = f'days_to_{date_column_name.lower().replace("_date", "")}'
        
        # Create bins starting at -1 to include 0-day items
        bins = [-1] + BUCKET_THRESHOLDS
        
        # Assign bucket labels based on days remaining
        df['bucket'] = pd.cut(
            df[days_col],
            bins=bins,
            labels=BUCKET_LABELS,
            right=True,
            include_lowest=True
        )
        
        # Handle items outside defined buckets
        df['bucket'] = df['bucket'].cat.add_categories('Non-Sensitive').fillna('Non-Sensitive')
        
        # Pivot: Sum amounts by Bucket and Type
        bucketed_data = df.groupby(['bucket', 'type'])['amount'].sum().unstack(fill_value=0)
        
        # Ensure all buckets and columns exist
        all_buckets = BUCKET_LABELS + ['Non-Sensitive']
        bucketed_data = bucketed_data.reindex(all_buckets, fill_value=0)
        
        if 'Asset' not in bucketed_data.columns: bucketed_data['Asset'] = 0
        if 'Liability' not in bucketed_data.columns: bucketed_data['Liability'] = 0
            
        bucketed_data.rename(columns={'Asset': 'Assets', 'Liability': 'Liabilities'}, inplace=True)
        
        return bucketed_data[['Assets', 'Liabilities']]

    def calculate_gap(self, date_column_name):
        """Calculates Static (per bucket) and Cumulative gaps."""
        bucketed_df = self._bucket_cashflows(date_column_name)
        
        # 1. Static Gap Calculation: Assets - Liabilities
        bucketed_df['Static Gap'] = bucketed_df['Assets'] - bucketed_df['Liabilities']
        
        # 2. Cumulative Gap Calculation: Running total of Static Gap
        time_buckets = bucketed_df.loc[BUCKET_LABELS]
        bucketed_df['Cumulative Gap'] = time_buckets['Static Gap'].cumsum().reindex(bucketed_df.index).fillna(0)

        return bucketed_df

    def get_liquidity_gap(self):
        return self.calculate_gap('maturity_date')

    def get_repricing_gap(self):
        return self.calculate_gap('repricing_date')