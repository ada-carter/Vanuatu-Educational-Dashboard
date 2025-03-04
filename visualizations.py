import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
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

def create_teacher_distribution(data):
    """Creates an enhanced stacked bar chart showing teacher distribution."""
    teacher_summary = data.groupby(['Province', 'Gender']).agg({
        'ECE': 'sum',
        'PS': 'sum',
        'PSET': 'sum',
        'SC': 'sum',
        'SS': 'sum'
    }).reset_index()
    
    fig = px.bar(teacher_summary,
                 x='Province',
                 y=['ECE', 'PS', 'PSET', 'SC', 'SS'],
                 color='Gender',
                 title='Teacher Distribution by Province, Level, and Gender',
                 labels={'value': 'Number of Teachers', 'variable': 'Education Level'},
                 barmode='group',
                 color_discrete_map={'F': '#ff9999', 'M': '#66b3ff'})
    
    fig.update_layout(
        xaxis_title="Province",
        yaxis_title="Number of Teachers",
        legend_title="Education Level / Gender"
    )
    
    return fig

def create_gender_ratio_plot(data, data_type="enrollment"):
    """Creates an enhanced bar chart comparing gender ratios with map."""
    try:
        if data_type == "enrollment":
            gender_data = data[data['Province'].isin(['F', 'M'])].copy()
            gender_summary = gender_data.groupby('Province')['Total'].sum().reset_index()
        elif data_type == "teacher":
            gender_summary = data.groupby(['Province', 'Gender'])['Total'].sum().unstack().reset_index()
            gender_summary['Ratio'] = gender_summary['F'] / (gender_summary['F'] + gender_summary['M'])
        
        fig = px.bar(gender_summary,
                    x='Province',
                    y=['F', 'M'] if data_type == "teacher" else 'Total',
                    title=f'Gender Distribution by Province ({data_type.title()})',
                    barmode='group',
                    color_discrete_map={'F': '#ff9999', 'M': '#66b3ff'})
        
        fig.update_layout(
            xaxis_title="Province",
            yaxis_title="Count",
            legend_title="Gender"
        )
        
        return fig
    except Exception as e:
        print(f"Error in create_gender_ratio_plot: {e}")
        return None

def create_enrollment_heatmap(data):
    """Creates a heatmap of enrollment numbers."""
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    fig = go.Figure(data=go.Heatmap(
        z=data[numeric_cols].values,
        x=numeric_cols,
        y=data.iloc[:, 0],  # First column contains Province names
        colorscale='RdYlBu'))
    fig.update_layout(title='Enrollment Heatmap by Grade and Province')
    return fig

def create_percentage_plot(data, year_cols):
    """Creates a plot showing percentages over time."""
    if not all(col in data.columns for col in year_cols):
        available_cols = [col for col in year_cols if col in data.columns]
        year_cols = available_cols
    
    fig = px.line(data, 
                  x=data.index,
                  y=year_cols,
                  title='Percentage Trends Over Time',
                  labels={'value': 'Percentage', 'variable': 'Year'})
    return fig

def create_age_distribution_analysis(data):
    """Creates an enhanced visualization for age distribution analysis."""
    # Pivot and aggregate the data
    age_pivot = data.pivot_table(
        values='Total',
        index=['Year', 'Province'],
        columns='Age',
        fill_value=0
    ).reset_index()
    
    # Create age group categories
    age_groups = {
        'Under 3': [0, 1, 2],
        '3-4 years': [3, 4],
        '5-6 years': [5, 6],
        'Over 6': [7, 8, 9, 10, 11]
    }
    
    # Calculate totals for each age group
    for group, ages in age_groups.items():
        age_pivot[group] = age_pivot[ages].sum(axis=1)
    
    # Melt the data for visualization
    plot_data = pd.melt(
        age_pivot,
        id_vars=['Year', 'Province'],
        value_vars=list(age_groups.keys()),
        var_name='Age Group',
        value_name='Number of Students'
    )
    
    # Create the visualization
    fig = px.bar(
        plot_data,
        x='Province',
        y='Number of Students',
        color='Age Group',
        facet_row='Year',
        barmode='stack',
        title='Age Distribution by Province (2018-2020)',
        labels={'Number of Students': 'Number of Enrolled Students'},
        category_orders={"Age Group": list(age_groups.keys())},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Update layout for better readability
    fig.update_layout(
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Province")
    fig.update_yaxes(title_text="Number of Students")
    
    return fig

def create_population_trend_visualization(population_data, school_age_only=False):
    """Creates a visualization of population trends with option to show only school-age groups."""
    # Define age groups to show
    if school_age_only:
        age_groups = ['0--4', '5--9', '10--14', '15--19']
    else:
        age_groups = [col for col in population_data.columns if '--' in col]

    # Convert Year to string to force categorical treatment
    population_data = population_data.copy()
    population_data['Year'] = population_data['Year'].astype(str)

    # Melt the dataframe for plotting
    melted_data = population_data.melt(
        id_vars=['Year'],
        value_vars=age_groups,
        var_name='Age Group',
        value_name='Population'
    )

    # Create stacked bar chart
    fig = px.bar(
        melted_data,
        x='Year',
        y='Population',
        color='Age Group',
        title='Population Distribution by Age Group in Vanuatu (2009-2020)',
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3,
        category_orders={"Year": ["2009", "2016", "2020"]}  # Force specific order
    )

    # Update layout
    fig.update_layout(
        yaxis=dict(title='Population'),
        xaxis=dict(
            title='Year',
            type='category',  # Force categorical axis
            tickmode='array',
            tickvals=['2009', '2016', '2020'],
            ticktext=['2009', '2016', '2020']
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        margin=dict(t=60),
        showlegend=True,
    )

    # Add gridlines for better readability
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig
