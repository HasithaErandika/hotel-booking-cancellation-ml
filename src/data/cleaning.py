import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw hotel bookings DataFrame.

    Creates a copy of the input DataFrame, removes target leakage columns
    ('reservation_status', 'reservation_status_date'), drops duplicate rows,
    prints a summary of removed records/columns, and returns the cleaned DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Raw or ingested hotel booking DataFrame.

    Returns
    -------
    pd.DataFrame
        Cleaned hotel booking DataFrame ready for validation and downstream processing.
    """
    cleaned_df = df.copy()

    initial_rows = len(cleaned_df)
    initial_cols = cleaned_df.shape[1]

    # Target leakage columns to drop
    leakage_cols = ["reservation_status", "reservation_status_date"]
    dropped_leakage = [col for col in leakage_cols if col in cleaned_df.columns]
    if dropped_leakage:
        cleaned_df = cleaned_df.drop(columns=dropped_leakage)

    # Drop duplicate rows
    duplicates_count = cleaned_df.duplicated().sum()
    cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)

    final_rows = len(cleaned_df)
    final_cols = cleaned_df.shape[1]

    print("=== Data Cleaning Summary ===")
    print(f"Initial Shape: {initial_rows} rows x {initial_cols} columns")
    print(f"Dropped Leakage Columns ({len(dropped_leakage)}): {dropped_leakage}")
    print(f"Dropped Duplicate Rows: {duplicates_count}")
    print(f"Final Cleaned Shape: {final_rows} rows x {final_cols} columns")
    print("==============================")

    return cleaned_df
