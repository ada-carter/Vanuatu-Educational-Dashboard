import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import json
import streamlit as st
from data.province_coordinates import PROVINCE_COLORS

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

def load_province_shapes():
    """Load and process Vanuatu province shapefiles."""
    try:
        # Read the shapefile
        gdf = gpd.read_file('data/shapefiles/vut_admbnda_adm1_spc_20180824/vut_admbnda_adm1_spc_20180824.shp')
        
        # Convert to GeoJSON for Plotly
        geojson = json.loads(gdf.to_json())
        
        # Create a mapping between province names and ADM1_EN
        province_mapping = {
            'Torba': 'TORBA',
            'Sanma': 'SANMA',
            'Penama': 'PENAMA',
            'Malampa': 'MALAMPA',
            'Shefa': 'SHEFA',
            'Tafea': 'TAFEA'
        }
        
        return geojson, province_mapping
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        return None, None

def create_map_visualization(data, values_column, title):
    """Creates a choropleth map visualization of Vanuatu provinces using actual shapefiles."""
    try:
        # Remove 'National' row if it exists and create a copy
        data = data[data['Province'] != 'National'].copy()
        
        # Load shapefile data
        gdf = gpd.read_file('data/shapefiles/vut_admbnda_adm1_spc_20180824/vut_admbnda_adm1_spc_20180824.shp')
        
        # Convert to a projected CRS (EPSG:3832 - Vanuatu 1960 / UTM zone 58S)
        gdf = gdf.to_crs(epsg=3832)
        
        # Create province mapping
        province_mapping = {
            'TORBA': 'Torba',
            'SANMA': 'Sanma', 
            'PENAMA': 'Penama',
            'MALAMPA': 'Malampa',
            'SHEFA': 'Shefa',
            'TAFEA': 'Tafea'
        }
        
        # Map province names
        gdf['Province'] = gdf['ADM1_EN'].map(province_mapping)
        
        # Merge data with geodataframe
        gdf = gdf.merge(data, on='Province', how='left')
        
        # Convert back to WGS 84 for plotting
        gdf = gdf.to_crs(epsg=4326)
        
        # Get bounds
        bounds = gdf.total_bounds  # returns (minx, miny, maxx, maxy)
        
        # Create the choropleth map
        fig = px.choropleth_mapbox(
            gdf,
            geojson=gdf.__geo_interface__,
            locations=gdf.index,
            color=values_column,
            color_continuous_scale='Viridis',
            mapbox_style='carto-positron',
            center={'lat': -15.3767, 'lon': 166.9592},  # Center of Vanuatu
            zoom=5,
            opacity=0.7,
            title=title,
            labels={values_column: 'Value'}
        )

        # Update layout
        fig.update_layout(
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            height=600,
            mapbox=dict(
                bounds=dict(
                    west=bounds[0],
                    east=bounds[2],
                    south=bounds[1],
                    north=bounds[3]
                )
            )
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating map visualization: {e}")
        # Create a simple fallback figure
        return px.scatter(data, x='Province', y=values_column, title=f"{title} (Map Unavailable)")

def create_enrollment_trend(data):
    """Creates an enhanced line plot showing enrollment trends."""
    data_melted = pd.melt(data, 
                         id_vars=['Year', 'Province'], 
                         value_vars=['Female', 'Male'],
                         var_name='Gender',
                         value_name='Enrollment')
    
    fig = px.line(data_melted,
                  x='Year',
                  y='Enrollment',
                  color='Province',
                  line_dash='Gender',
                  title='Enrollment Trends by Province and Gender',
                  labels={'Enrollment': 'Number of Students'},
                  color_discrete_map=PROVINCE_COLORS)
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Students",
        legend_title="Province / Gender"
    )
    
    return fig

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
