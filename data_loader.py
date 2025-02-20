import pandas as pd
import numpy as np
import os

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

def load_data():
    """Loads data from individual CSV files."""
    try:
        data_dir = "data"
        data = {
            "NER for ECCE": pd.read_csv(os.path.join(data_dir, "ner_ecce.csv")),
            "Enrollment by School Type": pd.read_csv(os.path.join(data_dir, "enrollment_by_school.csv")),
            "Detailed Enrollment": pd.read_csv(os.path.join(data_dir, "detailed_enrollment.csv")),
            "Teachers Distribution": pd.read_csv(os.path.join(data_dir, "teacher_distribution.csv")),
            "Age Distribution": pd.read_csv(os.path.join(data_dir, "age_distribution.csv"))
        }
        # Clean percentage values in 'NER for ECCE' table
        for col in data["NER for ECCE"].columns[2:]:
            data["NER for ECCE"][col] = data["NER for ECCE"][col].apply(clean_percentage)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        raise Exception(f"Error loading data: {str(e)}")
