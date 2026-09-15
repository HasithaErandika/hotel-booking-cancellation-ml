import pandas as pd


def validate_schema(df: pd.DataFrame) -> None:
    """Validate schema rules and target leakage assertions on the DataFrame.

    Ensures that 'is_canceled' exists in the DataFrame and that 'reservation_status'
    does not exist.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    Raises
    ------
    AssertionError
        If 'is_canceled' is missing or 'reservation_status' is present.
    """
    assert "is_canceled" in df.columns, (
        "Validation Error: Required target column 'is_canceled' is missing from DataFrame."
    )
    assert "reservation_status" not in df.columns, (
        "Validation Error: Target leakage column 'reservation_status' must NOT be present in DataFrame."
    )
    print("Schema validation passed: 'is_canceled' is present and 'reservation_status' is excluded.")
