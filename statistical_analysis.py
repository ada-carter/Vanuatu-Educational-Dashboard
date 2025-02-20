import pandas as pd

def calculate_summary_statistics(data: pd.DataFrame, column: str):
    """
    Calculates summary statistics for a given column in a DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The column for which to calculate statistics.

    Returns:
        pd.Series: A Series containing the summary statistics.
    """
    try:
        summary_statistics = data[column].describe()
        return summary_statistics
    except KeyError:
        return f"Column '{column}' not found in the data."
    except Exception as e:
        return f"Error calculating summary statistics: {e}"
