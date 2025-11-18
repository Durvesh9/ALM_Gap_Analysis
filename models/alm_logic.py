import pandas as pd
from config import ANALYSIS_DATE, BUCKET_LABELS, BUCKET_THRESHOLDS

class ALMGapAnalyzer:
    def __init__(self, data_df):
        self.data_df = data_df.copy()
        if self.data_df.empty:
            print("WARNING: Analyzer initialized with empty data.")
        
        self._prepare_data()

    def _prepare_data(self):
        """Calculates days-to-maturity and days-to-repricing."""
        current_date = pd.to_datetime(ANALYSIS_DATE)
        
        self.data_df['days_to_maturity'] = (self.data_df['maturity_date'] - current_date).dt.days
        self.data_df['days_to_repricing'] = (self.data_df['repricing_date'] - current_date).dt.days
        
        # Normalize type: Assets are positive cashflows, Liabilities are negative
        self.data_df['amount_signed'] = self.data_df.apply(
            lambda row: row['amount'] if row['type'] == 'Asset' else -row['amount'], 
            axis=1
        )
        print("INFO: Data prepared with day counts and signed amounts.")

    def _bucket_cashflows(self, date_column_name):
        """Buckets amounts based on the specified date column (Maturity or Repricing)."""
        df = self.data_df.copy()
        days_col = f'days_to_{date_column_name.lower().replace("_date", "")}'
        
        # --- FIX APPLIED HERE ---
        # Original: bins=[0] + BUCKET_THRESHOLDS
        # Correction: Use -1 as the starting bin to correctly capture instruments maturing/repricing TODAY (0 days difference) 
        # in the 'Overnight' bucket [0, 1].
        df['bucket'] = pd.cut(
            df[days_col],
            bins=[-1] + BUCKET_THRESHOLDS,
            labels=BUCKET_LABELS,
            right=True, 
            include_lowest=True
        )

        df['bucket'] = df['bucket'].cat.add_categories('Non-Sensitive').fillna('Non-Sensitive')
        
        bucketed_data = df.groupby(['bucket', 'type'])['amount'].sum().unstack(fill_value=0)
        
        all_buckets = BUCKET_LABELS + ['Non-Sensitive']
        bucketed_data = bucketed_data.reindex(all_buckets, fill_value=0)

        if 'Asset' not in bucketed_data.columns: bucketed_data['Asset'] = 0
        if 'Liability' not in bucketed_data.columns: bucketed_data['Liability'] = 0
            
        bucketed_data.rename(columns={'Asset': 'Assets', 'Liability': 'Liabilities'}, inplace=True)
        print(f"INFO: Cashflows successfully bucketed by {date_column_name}.")
        return bucketed_data[['Assets', 'Liabilities']]

    def calculate_gap(self, date_column_name):
        """Calculates the static and cumulative gap for the specified date column."""
        bucketed_df = self._bucket_cashflows(date_column_name)
        
        # 1. Calculate Static Gap (A - L)
        bucketed_df['Static Gap'] = bucketed_df['Assets'] - bucketed_df['Liabilities']
        
        # 2. Calculate Cumulative Gap
        # Only accumulate over the time buckets (excluding 'Non-Sensitive')
        time_buckets = bucketed_df.loc[BUCKET_LABELS]
        cumulative_gap = time_buckets['Static Gap'].cumsum()
        
        # Reindex to place the cumulative values back into the main DF structure
        bucketed_df['Cumulative Gap'] = cumulative_gap.reindex(bucketed_df.index).fillna(0)

        print(f"INFO: Static and Cumulative Gap calculated for {date_column_name}.")
        return bucketed_df

    def get_liquidity_gap(self):
        return self.calculate_gap('maturity_date')

    def get_repricing_gap(self):
        return self.calculate_gap('repricing_date')