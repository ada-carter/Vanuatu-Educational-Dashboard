import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
from visualizations import create_bar_chart, create_scatter_plot, display_table
from statistical_analysis import calculate_summary_statistics

# Set page configuration
st.set_page_config(layout="wide")

# Load data
try:
    all_data = load_data("VData.csv")
except FileNotFoundError:
    st.error("Error: 'VData.csv' not found. Please ensure the file is in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Main content
st.title("Vanuatu Educational Dashboard")

# Data Overview
st.header("Data Overview")
for table_name, data in all_data.items():
    st.subheader(f"Table: {table_name}")
    st.dataframe(data.head())

    # Visualizations
    st.header(f"Visualizations for Table: {table_name}")
    numeric_columns = data.select_dtypes(include=['number']).columns

    if not numeric_columns.empty:
        for column in numeric_columns:
            # Bar Chart
            st.subheader(f"Bar Chart of {column} in {table_name}")
            try:
                bar_chart = create_bar_chart(data, column)
                if bar_chart:  # Check if the chart was created successfully
                    st.plotly_chart(bar_chart, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating bar chart for {column} in {table_name}: {e}")

            # Scatter Plot
            st.subheader(f"Scatter Plot of {column} in {table_name}")
            try:
                scatter_plot = create_scatter_plot(data, column)
                if scatter_plot:  # Check if the chart was created successfully
                    st.plotly_chart(scatter_plot, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating scatter plot for {column} in {table_name}: {e}")
    else:
        st.warning(f"No numeric columns found in table '{table_name}'.")

    # Statistical Analysis
    st.header(f"Statistical Analysis for Table: {table_name}")
    if not numeric_columns.empty:
        for column in numeric_columns:
            try:
                st.subheader(f"Summary Statistics for {column} in {table_name}")
                summary_statistics = calculate_summary_statistics(data, column)
                st.write(summary_statistics)
            except Exception as e:
                st.error(f"Error calculating summary statistics for {column} in {table_name}: {e}")
    else:
        st.warning(f"No statistical analysis available for table '{table_name}' (no numeric columns).")

    # Data Table
    st.header(f"Data Table: {table_name}")
    display_table(data)
