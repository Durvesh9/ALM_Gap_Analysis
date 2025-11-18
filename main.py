from utils.database import get_db_engine, setup_database, load_data_to_db, fetch_data_from_db
from models.alm_logic import ALMGapAnalyzer
from models.scenarios import calculate_nii_sensitivity
from utils.reporting import plot_gap_profile, export_to_excel

def main():
    """Main function to execute the ALM Gap Analysis tool."""
    print("\n--- Starting ALM Gap Analysis Tool ---")

    # 1. Database Connection and Setup
    engine = get_db_engine()
    if engine is None:
        print("FATAL ERROR: Failed to establish database connection. Exiting.")
        return

    setup_database(engine)
    load_data_to_db(engine)

    # 2. Fetch Data and Initialize Analyzer
    data_df = fetch_data_from_db(engine)
    if data_df.empty:
        print("FATAL ERROR: No valid data retrieved from the database. Exiting.")
        return
    
    analyzer = ALMGapAnalyzer(data_df)

    # 3. Gap Analysis
    print("\n--- Performing Gap Analysis ---")
    
    # a. Liquidity Gap
    liquidity_gap_df = analyzer.get_liquidity_gap()
    print("\nLiquidity Gap Results (Maturity):\n", liquidity_gap_df)
    
    # b. Repricing Gap
    repricing_gap_df = analyzer.get_repricing_gap()
    print("\nRepricing Gap Results (Rate Reset):\n", repricing_gap_df)

    # 4. Scenario Analysis (IRRBB)
    print("\n--- Performing Scenario Analysis (NII Sensitivity) ---")
    nii_sensitivity_df = calculate_nii_sensitivity(repricing_gap_df)
    print("\nNII Sensitivity Results:\n", nii_sensitivity_df)

    # 5. Reporting and Visualization
    print("\n--- Generating Reports ---")

    # a. Plots
    plot_gap_profile(liquidity_gap_df, "Liquidity")
    plot_gap_profile(repricing_gap_df, "Repricing")

    # b. Excel Export
    export_to_excel(liquidity_gap_df, repricing_gap_df, nii_sensitivity_df)

    print("\n--- ALM Analysis Complete ---")
    print("Review the 'output' folder for the Excel report and visualizations.")


if __name__ == "__main__":
    main()  