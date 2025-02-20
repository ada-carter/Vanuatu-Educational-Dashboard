import pandas as pd
import numpy as np

def clean_percentage(value):
    """Clean percentage values and convert to float."""
    if isinstance(value, str):
        value = value.strip().rstrip('%')
        try:
            return float(value) / 100
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
            
            # Clean and set headers
            if table_name == "NER for ECCE":
                # Skip first row (title), use second row as header
                headers = ['Province', 'School_Type'] + ['Female_2018', 'Male_2018', 'Total_2018',
                                                       'Female_2019', 'Male_2019', 'Total_2019',
                                                       'Female_2020', 'Male_2020', 'Total_2020']
                table = table.iloc[2:].copy()
                table.columns = headers
                # Convert percentages to floats
                for col in table.columns[2:]:
                    table[col] = table[col].apply(clean_percentage)
            
            elif table_name == "Enrollment by School Type":
                # Use first row as header
                table = table.iloc[1:].copy()
                table.columns = ['School_Type', 'ECCE', 'Primary', 'Secondary', 'Total']
                # Convert to numeric
                for col in table.columns[1:]:
                    table[col] = pd.to_numeric(table[col], errors='coerce')
            
            elif table_name == "Detailed Enrollment":
                # Use meaningful column names
                headers = ['Province'] + ['PreSchool'] + [f'Grade_{i}' for i in range(1, 7)] + \
                         ['Primary_Total'] + [f'Grade_{i}' for i in range(7, 15)] + \
                         ['Secondary_Total', 'Total']
                table = table.iloc[1:].copy()
                table.columns = headers
                # Convert to numeric
                for col in table.columns[1:]:
                    table[col] = pd.to_numeric(table[col].str.replace(',', ''), errors='coerce')
            
            elif table_name == "Teachers Distribution":
                # Skip header row and use meaningful names
                headers = ['Province', 'Gender', 'ECE', 'PS', 'PSET', 'SC', 'SS', 'Total']
                table = table.iloc[1:].copy()
                table.columns = headers
                # Convert to numeric
                for col in table.columns[2:]:
                    table[col] = pd.to_numeric(table[col], errors='coerce')
            
            elif table_name == "Age Distribution":
                # Use meaningful column names
                headers = ['Year_Age'] + ['Female', 'Male', 'Total'] * 6 + ['Vanuatu_Total']
                table = table.iloc[1:].copy()
                table.columns = headers
                # Convert to numeric
                for col in table.columns[1:]:
                    table[col] = pd.to_numeric(table[col].str.replace(',', ''), errors='coerce')
            
            # Reset index
            table = table.reset_index(drop=True)
            data[table_name] = table
            
        return data
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")
