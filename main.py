from utils.database import get_db_engine, setup_database, load_data_to_db, fetch_data_from_db
# Imported the new get_detailed_view function
from models.alm_logic import prepare_data, get_liquidity_gap, get_repricing_gap, get_detailed_view
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

    # 2. Fetch Data
    data_df = fetch_data_from_db(engine)
    if data_df.empty:
        print("FATAL ERROR: No valid data retrieved from the database. Exiting.")
        return
    
    # 3. Prepare Data
    prepared_df = prepare_data(data_df)

    # 4. Gap Analysis (Summary Level)
    print("\n--- Performing Gap Analysis ---")
    
    liquidity_gap_df = get_liquidity_gap(prepared_df)
    print("\nLiquidity Gap Results (Maturity):\n", liquidity_gap_df)
    
    repricing_gap_df = get_repricing_gap(prepared_df)
    print("\nRepricing Gap Results (Rate Reset):\n", repricing_gap_df)

    # 5. Scenario Analysis (IRRBB)
    print("\n--- Performing Scenario Analysis (NII Sensitivity) ---")
    nii_sensitivity_df = calculate_nii_sensitivity(repricing_gap_df)
    print("\nNII Sensitivity Results:\n", nii_sensitivity_df)

    # 6. Generate Detailed Audit Data
    print("\n--- Generating Detailed Audit Data ---")
    detailed_audit_df = get_detailed_view(prepared_df)

    # 7. Reporting and Visualization
    print("\n--- Generating Reports ---")

    plot_gap_profile(liquidity_gap_df, "Liquidity")
    plot_gap_profile(repricing_gap_df, "Repricing")

    # Pass the detailed audit data to the excel export
    export_to_excel(liquidity_gap_df, repricing_gap_df, nii_sensitivity_df, detailed_audit_df)

    print("\n--- ALM Analysis Complete ---")
    print("Review the 'output' folder for the Excel report containing raw data and visualizations.")

if __name__ == "__main__":
    main()