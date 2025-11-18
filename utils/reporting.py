import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from config import BUCKET_LABELS, OUTPUT_DIR, OUTPUT_FILE_PATH

def setup_output_directory():
    """Ensures the output directory exists using pathlib."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"INFO: Output directory ensured: {OUTPUT_DIR}")

def plot_gap_profile(gap_df, gap_type):
    """Generates and saves a stacked bar chart for the gap profile."""
    
    setup_output_directory()
    title = f'{gap_type} Gap Profile (Assets minus Liabilities)'
    file_name = Path(OUTPUT_DIR) / f'{gap_type.lower().replace(" ", "_")}_gap.png'
    
    try:
        plt.figure(figsize=(12, 6))
        
        # Plot the absolute gap
        gap_df['Static Gap'].plot(kind='bar', 
                                  color=gap_df['Static Gap'].apply(lambda x: 'g' if x >= 0 else 'r'))
        
        plt.axhline(0, color='grey', linewidth=0.8)
        plt.title(title, fontsize=16)
        plt.ylabel('Amount (Currency Units)')
        plt.xlabel('Time Bucket')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(file_name)
        plt.close()
        print(f"INFO: Generated plot: {file_name}")
    except Exception as e:
        print(f"ERROR generating {gap_type} plot: {e}")

def export_to_excel(gap_liquidity, gap_repricing, nii_sensitivity):
    """Exports all analysis results to a multi-sheet Excel file."""
    
    setup_output_directory()
    
    try:
        with pd.ExcelWriter(OUTPUT_FILE_PATH, engine='openpyxl') as writer:
            gap_liquidity.to_excel(writer, sheet_name='Liquidity Gap', index=True)
            gap_repricing.to_excel(writer, sheet_name='Repricing Gap', index=True)
            nii_sensitivity.to_excel(writer, sheet_name='NII Sensitivity', index=True)
            
        print(f"INFO: Successfully exported results to Excel: {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"ERROR exporting data to Excel: {e}")