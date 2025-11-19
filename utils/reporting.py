import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from config import OUTPUT_DIR, OUTPUT_FILE_PATH

def setup_output_directory():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def plot_gap_profile(gap_df, gap_type):
    setup_output_directory()
    file_name = Path(OUTPUT_DIR) / f'{gap_type.lower().replace(" ", "_")}_gap.png'
    
    try:
        plt.figure(figsize=(12, 6))
        bar_colors = gap_df['Static Gap'].apply(lambda x: 'green' if x >= 0 else 'red')
        gap_df['Static Gap'].plot(kind='bar', color=bar_colors)
        plt.axhline(0, color='grey', linewidth=0.8)
        plt.title(f'{gap_type} Gap Profile', fontsize=16)
        plt.ylabel('Amount')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(file_name)
        plt.close()
        print(f"INFO: Chart saved to {file_name}")
    except Exception as e:
        print(f"ERROR plotting chart: {e}")

# --- UPDATED EXPORT FUNCTION ---
def export_to_excel(gap_liquidity, gap_repricing, nii_sensitivity, detailed_data):
    """
    Exports all analysis results AND the raw detailed data to Excel.
    """
    setup_output_directory()
    
    try:
        with pd.ExcelWriter(OUTPUT_FILE_PATH, engine='openpyxl') as writer:
            # 1. The Summaries
            gap_liquidity.to_excel(writer, sheet_name='Liquidity Gap')
            gap_repricing.to_excel(writer, sheet_name='Repricing Gap')
            nii_sensitivity.to_excel(writer, sheet_name='NII Sensitivity')
            
            # 2. The Detailed Data (Audit Trail)
            detailed_data.to_excel(writer, sheet_name='Detailed Calculation Data', index=False)
            
        print(f"INFO: Successfully exported results including DETAILED DATA to: {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"ERROR exporting data to Excel: {e}")