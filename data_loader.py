import pandas as pd

def load_data(file_path):
    """
    Loads data from a CSV file and extracts tables based on predefined coordinates.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary where keys are table names and values are pandas DataFrames.
    """
    try:
        df = pd.read_csv(file_path, header=None, encoding='utf-8')

        # Define table coordinates
        table_coordinates = {
            "Table 1: NER for ECCE": (0, 0, 10, 9),  # A1:J10
            "Table 2: Enrollment by School Type": (11, 0, 19, 3),  # A12:D19
            "Table 3: Detailed Enrollment Data": (20, 0, 37, 18),  # A21:S37
            "Table 4: Number of Teachers": (38, 0, 49, 6),  # A39:G49
            "Table 5: Age Distribution": (50, 0, 84, 19),  # A51:T84
        }

        data = {}
        for table_name, (start_row, start_col, end_row, end_col) in table_coordinates.items():
            table = df.iloc[start_row:end_row+1, start_col:end_col+1]
            # Reset index and column names
            table = table.reset_index(drop=True)
            table.columns = range(table.shape[1])  # Assign default column names
            data[table_name] = table

        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
