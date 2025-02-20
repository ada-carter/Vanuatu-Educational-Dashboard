import plotly.express as px
import pandas as pd
import streamlit as st

def create_bar_chart(data: pd.DataFrame, column: str):
    """
    Creates a bar chart using Plotly.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The column to be displayed on the bar chart.

    Returns:
        plotly.graph_objects.Figure: The bar chart figure.
    """
    try:
        fig = px.bar(data, x=data.index, y=column, title=f"Bar Chart of {column}")
        return fig
    except Exception as e:
        st.error(f"Error creating bar chart: {e}")
        return None

def create_scatter_plot(data: pd.DataFrame, column: str):
    """
    Creates a scatter plot using Plotly.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The column to be displayed on the scatter plot.

    Returns:
        plotly.graph_objects.Figure: The scatter plot figure.
    """
    try:
        fig = px.scatter(data, x=data.index, y=column, title=f"Scatter Plot of {column}")
        return fig
    except Exception as e:
        st.error(f"Error creating scatter plot: {e}")
        return None

def display_table(data: pd.DataFrame):
    """
    Displays a pandas DataFrame as a Streamlit table.

    Args:
        data (pd.DataFrame): The DataFrame to be displayed.
    """
    st.dataframe(data)
