import pandas as pd

def load_data(file_path):
    """
    Loads data from a CSV file and extracts tables based on predefined coordinates.
    Correctly infers headers and handles data types, and handles duplicate column names.

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
            table = df.iloc[start_row:end_row+1, start_col:end_col+1].copy()

            # Infer header row
            header_row = table.iloc[0]
            # Check if the first element of the header row is the table name itself
            if header_row.iloc[0] == df.iloc[start_row, start_col]:
                table = table[2:]  # Skip the first two rows
                header_row = df.iloc[start_row+1, start_col:end_col+1] #Real Header
            else:
                table = table[1:]  # Skip the first row
            table.columns = header_row

            # Reset index
            table = table.reset_index(drop=True)

            # Clean and convert Table 1 to numeric
            if table_name == "Table 1: NER for ECCE":
                print(f"Column names before conversion: {table.columns}")  # Debugging
                for col in table.columns[2:]:  # Start from the third column (2018 onwards)
                    print(f"Data type of column {col} before conversion: {table[col].dtype}")  # Debugging
                    try:
                        table[col] = table[col].str.rstrip('%').astype('float') / 100
                    except Exception as e:
                        print(f"Error converting column {col}: {e}")  # Debugging

            # Try converting other tables to numeric where possible
            else:
                for col in table.columns:
                    try:
                        table[col] = pd.to_numeric(table[col])
                    except:
                        pass
            # Handle duplicate column names
            table.columns = pd.Series(table.columns).fillna('').astype(str)
            table = table.loc[:,~table.columns.duplicated()].copy()

            data[table_name] = table

        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
