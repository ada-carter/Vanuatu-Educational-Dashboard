import plotly.express as px
import plotly.graph_objects as go
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

def create_enrollment_trend(data):
    """Creates a line plot showing enrollment trends by province."""
    fig = px.line(data, 
                  x='Year_Age', 
                  y=['Female', 'Male', 'Total'],
                  title='Enrollment Trends by Gender',
                  labels={'value': 'Number of Students', 'variable': 'Gender'})
    return fig

def create_teacher_distribution(data):
    """Creates a stacked bar chart showing teacher distribution."""
    fig = px.bar(data, 
                 x='Province', 
                 y=['ECE', 'PS', 'PSET', 'SC', 'SS'],
                 title='Teacher Distribution by Province and Level',
                 labels={'value': 'Number of Teachers', 'variable': 'Education Level'},
                 barmode='stack')
    return fig

def create_gender_ratio_plot(data):
    """Creates a bar chart comparing gender ratios."""
    fig = px.bar(data, 
                 x='Province',
                 y=['Female', 'Male'],
                 title='Gender Distribution by Province',
                 barmode='group')
    return fig

def create_enrollment_heatmap(data):
    """Creates a heatmap of enrollment numbers."""
    fig = go.Figure(data=go.Heatmap(
        z=data.iloc[:, 1:-1],
        x=data.columns[1:-1],
        y=data['Province'],
        colorscale='RdYlBu'))
    fig.update_layout(title='Enrollment Heatmap by Grade and Province')
    return fig

def create_percentage_plot(data, year_cols):
    """Creates a plot showing percentages over time."""
    fig = px.line(data, 
                  x=data.index, 
                  y=year_cols,
                  title='Percentage Trends Over Time',
                  labels={'value': 'Percentage', 'variable': 'Year'})
    return fig
