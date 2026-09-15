import os
from pathlib import Path
from typing import Union
import pandas as pd


def load_raw_data(filepath: Union[str, Path] = "data/hotel_bookings.csv") -> pd.DataFrame:
    """Load raw hotel booking data from a CSV file.

    Parameters
    ----------
    filepath : Union[str, Path], default="data/hotel_bookings.csv"
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded raw hotel booking dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the specified path.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {path.resolve()}")

    df = pd.read_csv(path)
    return df
