import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from config import OUTPUT_DIR, OUTPUT_FILE_PATH

def setup_output_directory():
    """Creates the output folder."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def plot_gap_profile(gap_df, gap_type):
    """Generates and saves a bar chart for the Static Gap."""
    setup_output_directory()
    
    file_name = Path(OUTPUT_DIR) / f'{gap_type.lower().replace(" ", "_")}_gap.png'
    
    try:
        plt.figure(figsize=(12, 6))
        
        # Color positive gaps Green, negative gaps Red
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

def export_to_excel(gap_liquidity, gap_repricing, nii_sensitivity):
    """Exports the three analysis dataframes to a single Excel file."""
    setup_output_directory()
    
    try:
        with pd.ExcelWriter(OUTPUT_FILE_PATH, engine='openpyxl') as writer:
            gap_liquidity.to_excel(writer, sheet_name='Liquidity Gap')
            gap_repricing.to_excel(writer, sheet_name='Repricing Gap')
            nii_sensitivity.to_excel(writer, sheet_name='NII Sensitivity')
            
        print(f"INFO: Report saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"ERROR saving Excel: {e}")