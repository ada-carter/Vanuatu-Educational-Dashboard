import pandas as pd
import numpy as np

def clean_percentage(value):
    """Clean percentage values and convert to float."""
    if pd.isna(value):
        return np.nan
    if isinstance(value, str):
        try:
            # Remove percentage sign and convert to float
            return float(value.strip().rstrip('%')) / 100.0
        except ValueError:
            return np.nan
    return value

def load_data(file_path):
    """Loads and preprocesses data from CSV file."""
    try:
        df = pd.read_csv(file_path, header=None, encoding='utf-8')
        
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
                # Skip the title row and use the second row as header
                headers = ['Province', 'School_Type']
                for year in ['2018', '2019', '2020']:
                    headers.extend([f'Female_{year}', f'Male_{year}', f'Total_{year}'])
                
                # Skip first two rows (title and year)
                table = table.iloc[2:].copy()
                table.columns = headers[:table.shape[1]]
                
                # Convert percentage strings to floats
                for col in table.columns[2:]:
                    table[col] = table[col].apply(clean_percentage)
            
            elif table_name == "Enrollment by School Type":
                # Use first row as header
                headers = ['School_Type', 'ECCE', 'Primary', 'Secondary']
                table = table.iloc[1:].copy()
                table = table.iloc[:, :len(headers)]
                table.columns = headers
                
                # Convert to numeric
                for col in table.columns[1:]:
                    table[col] = pd.to_numeric(table[col], errors='coerce')
            
            elif table_name == "Detailed Enrollment":
                # Get actual number of columns
                n_cols = table.shape[1]
                headers = ['Province', 'PreSchool', 'PreSchool_Total'] + \
                         [f'Grade_{i}' for i in range(1, 7)] + \
                         ['Primary_Total'] + [f'Grade_{i}' for i in range(7, 15)] + \
                         ['Secondary_Total', 'Total']
                headers = headers[:n_cols]  # Trim to match actual columns
                table = table.iloc[1:].copy()
                table.columns = headers
                for col in table.columns[1:]:
                    table[col] = pd.to_numeric(table[col].str.replace(',', ''), errors='coerce')
            
            elif table_name == "Teachers Distribution":
                headers = ['Province', 'Gender', 'ECE', 'PS', 'PSET', 'SC', 'SS', 'Total']
                table = table.iloc[1:].copy()
                table.columns = headers[:table.shape[1]]
                for col in table.columns[2:]:
                    table[col] = pd.to_numeric(table[col], errors='coerce')
            
            elif table_name == "Age Distribution":
                # Calculate the number of provinces (6) plus Vanuatu total
                n_regions = 7
                headers = ['Year_Age']
                for region in range(n_regions-1):  # Exclude Vanuatu total from loop
                    headers.extend(['Female', 'Male', 'Total'])
                headers.append('Vanuatu_Total')
                
                table = table.iloc[1:].copy()
                table.columns = headers[:table.shape[1]]
                for col in table.columns[1:]:
                    try:
                        table[col] = pd.to_numeric(table[col].str.replace(',', '').str.strip(), errors='coerce')
                    except AttributeError:
                        table[col] = pd.to_numeric(table[col], errors='coerce')
            
            # Reset index
            table = table.reset_index(drop=True)
            data[table_name] = table
        
        return data
    except Exception as e:
        print(f"Error in load_data: {str(e)}")  # Debug print
        raise Exception(f"Error loading data: {str(e)}")
