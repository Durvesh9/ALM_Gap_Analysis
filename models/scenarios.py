import pandas as pd
from config import RATE_SHOCKS

def calculate_nii_sensitivity(repricing_gap_df):
    """Calculates NII impact based on the 1-Year Cumulative Gap."""
    print("INFO: Starting NII Sensitivity calculation.")
    
    try:
        horizon_bucket = '1 Year'
        if horizon_bucket not in repricing_gap_df.index:
             raise ValueError("The '1 Year' bucket is missing.")
        
        # The position exposed to rate changes
        rate_sensitive_position = repricing_gap_df.loc[horizon_bucket, 'Cumulative Gap']
        
        nii_results = {}
        
        for shock_label, shock_bps in RATE_SHOCKS.items():
            # Calculation: Exposure * Rate Change
            change_in_nii = rate_sensitive_position * shock_bps
            nii_results[shock_label] = change_in_nii

        nii_df = pd.DataFrame.from_dict(
            nii_results, 
            orient='index', 
            columns=['Change in NII (1Y Horizon)']
        )
        
        nii_df.loc['Rate-Sensitive Position (1Y Gap)'] = rate_sensitive_position
        
        return nii_df

    except Exception as e:
        print(f"ERROR in NII sensitivity calculation: {e}")
        return pd.DataFrame()