import pandas as pd
from config import RATE_SHOCKS, BUCKET_LABELS

def calculate_nii_sensitivity(repricing_gap_df):
    """
    Simulates the impact of interest rate shocks on Net Interest Income (NII) 
    over a 1-year horizon.
    """
    print("INFO: Starting NII Sensitivity calculation.")
    
    try:
        # 1. Get the 1-Year Cumulative Gap
        horizon_bucket = '1 Year'
        if horizon_bucket not in repricing_gap_df.index:
             raise ValueError("The '1 Year' bucket is missing from the repricing gap analysis.")
             
        rate_sensitive_position = repricing_gap_df.loc[horizon_bucket, 'Cumulative Gap']
        
        nii_results = {}
        
        # 2. Calculate NII Change for each scenario
        for shock_label, shock_bps in RATE_SHOCKS.items():
            # Formula: Change in NII = Rate-Sensitive Position * Interest Rate Shock
            change_in_nii = rate_sensitive_position * shock_bps
            nii_results[shock_label] = change_in_nii
            print(f"INFO: Scenario '{shock_label}': Rate Shock={shock_bps:.2%}, Change in NII={change_in_nii:,.2f}")

        # 3. Format output
        nii_df = pd.DataFrame.from_dict(
            nii_results, 
            orient='index', 
            columns=['Change in NII (1Y Horizon)']
        )
        nii_df.index.name = 'Rate Shock Scenario'
        
        # Add the Rate-Sensitive Position for context
        nii_df.loc['Rate-Sensitive Position (1Y Gap)'] = rate_sensitive_position
        
        return nii_df

    except Exception as e:
        print(f"ERROR in NII sensitivity calculation: {e}")
        return pd.DataFrame()