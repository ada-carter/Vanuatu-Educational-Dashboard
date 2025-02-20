import pandas as pd
import numpy as np

def clean_percentage(value):
    """Clean percentage values and convert to float."""
    if pd.isna(value):
        return np.nan
    if isinstance(value, str):
        try:
            # Remove percentage sign, commas, and spaces, then convert to float
            cleaned = value.strip().rstrip('%').replace(',', '').strip()
            return float(cleaned) / 100.0 if '%' in value else float(cleaned)
        except ValueError:
            return np.nan
    return value

def load_data(file_path):
    """Loads and preprocesses data from CSV file."""
    try:
        # Read CSV with first row as header
        df = pd.read_csv(file_path)
        
        table_coordinates = {
            "NER for ECCE": (0, 0, 10, 9),
            "Enrollment by School Type": (11, 0, 19, 3),
            "Detailed Enrollment": (20, 0, 37, 18),
            "Teachers Distribution": (38, 0, 49, 6),
            "Age Distribution": (50, 0, 84, 19)
        }
        
        data = {}
        for table_name, (start_row, start_col, end_row, end_col) in table_coordinates.items():
            # Extract table
            table = df.iloc[start_row:end_row+1, start_col:end_col+1].copy()
            
            if table_name == "NER for ECCE":
                # Create fixed column names
                col_names = ['Province', 'School_Type']
                for year in ['2018', '2019', '2020']:
                    col_names.extend([f'Female_{year}', f'Male_{year}', f'Total_{year}'])
                # Slice the columns to match the actual data
                col_names = col_names[:table.shape[1]]
                
                # Skip first two rows and set column names
                table = table.iloc[2:].copy()
                table.columns = col_names
                
                # Convert percentages to floats
                for col in table.columns[2:]:
                    if col in table.columns:  # Check if column exists
                        table[col] = table[col].map(clean_percentage)
            
            elif table_name == "Enrollment by School Type":
                # Use known column names
                col_names = ['School_Type', 'ECCE', 'Primary', 'Secondary']
                table = table.iloc[1:, :len(col_names)].copy()
                table.columns = col_names
                
                # Convert numeric columns
                for col in table.columns[1:]:
                    table[col] = pd.to_numeric(table[col].astype(str).str.replace(',', ''), errors='coerce')
            
            elif table_name == "Detailed Enrollment":
                # Skip first row which contains headers
                table = table.iloc[1:].copy()
                # Convert numeric columns (all except first column)
                for col in range(1, table.shape[1]):
                    table.iloc[:, col] = pd.to_numeric(
                        table.iloc[:, col].astype(str).str.replace(',', ''),
                        errors='coerce'
                    )
            
            elif table_name == "Teachers Distribution":
                # Skip first row and use known column names
                table = table.iloc[1:].copy()
                col_names = ['Province', 'Gender', 'ECE', 'PS', 'PSET', 'SC', 'SS', 'Total']
                table.columns = col_names[:table.shape[1]]
                
                # Convert numeric columns
                for col in table.columns[2:]:
                    table[col] = pd.to_numeric(table[col], errors='coerce')
            
            elif table_name == "Age Distribution":
                # Skip first row
                table = table.iloc[1:].copy()
                # Convert numeric columns (all except Year column)
                for col in range(1, table.shape[1]):
                    table.iloc[:, col] = pd.to_numeric(
                        table.iloc[:, col].astype(str).str.replace(',', '').str.strip(),
                        errors='coerce'
                    )
            
            # Reset index
            table = table.reset_index(drop=True)
            data[table_name] = table
        
        return data
    except Exception as e:
        print(f"Error in load_data: {str(e)}")  # Debug print
        raise Exception(f"Error loading data: {str(e)}")
