import streamlit as st
import pandas as pd
import plotly.express as px
import os
from data_loader import load_data
from visualizations import *
from data.province_coordinates import PROVINCE_COLORS
import plotly.graph_objects as go

# Page configuration
st.set_page_config(layout="wide", page_title="Vanuatu Education Report 2020-2023")

# Load data
try:
    data = load_data()
    for key in ["Enrollment by School Type"]:
        if "Province" in data[key].columns:
            data[key] = data[key][data[key]["Province"] != "National"]
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Check for required files
shapefile_path = "data/shapefiles/vut_admbnda_adm1_spc_20180824/vut_admbnda_adm1_spc_20180824.shp"
if not os.path.exists(shapefile_path):
    st.error("Missing shapefile. Please ensure the province shapefiles exist in the data/shapefiles directory.")
    st.stop()

# Report Header
st.title("State of Education in Vanuatu: Comprehensive Analysis 2020-2023")
st.markdown("*A detailed examination of educational trends, challenges, and opportunities across Vanuatu's provinces*")

# Executive Summary
st.header("Executive Summary")
st.markdown("""
This report presents a comprehensive analysis of Vanuatu's education system, examining key metrics across all provinces.
The analysis reveals significant variations in educational access and quality between regions, with particular challenges
in remote areas and opportunities for improvement in specific sectors.

Key findings include:
- [Placeholder for key finding 1]
- [Placeholder for key finding 2]
- [Placeholder for key finding 3]
""")

# Vanuatu Context Section
st.header("Vanuatu in Global Context")

# Load HPI data
try:
    hpi_data = pd.read_csv("data/hpi.csv")
except Exception as e:
    st.error(f"Error loading HPI data: {e}")
    hpi_data = None

if hpi_data is not None:
    metrics = {
        'HPI': {'description': 'Happy Planet Index - measures sustainable wellbeing for all', 'inverse': False},
        'Life Expectancy in Years': {'description': 'Average number of years a person is expected to live', 'inverse': False},
        'Ladder Of Life': {'description': 'Subjective wellbeing score (0-10)', 'inverse': False},
        'Ecological Footprint': {'description': 'Per capita Ecological Footprint (global hectares) - lower is better', 'inverse': True}
    }
    
    # User input for country comparison
    user_country = st.text_input("Add a country for comparison:", "")
    
    # Create tabs for different metrics
    metric_tabs = st.tabs(list(metrics.keys()))
    
    for i, (metric, info) in enumerate(metrics.items()):
        with metric_tabs[i]:
            # Get Vanuatu's data
            vanuatu_data = hpi_data[hpi_data['country'] == 'Vanuatu'].copy()
            
            # Get top 9 excluding Vanuatu
            if info['inverse']:
                other_data = hpi_data[hpi_data['country'] != 'Vanuatu'].nsmallest(9, metric).copy()
            else:
                other_data = hpi_data[hpi_data['country'] != 'Vanuatu'].nlargest(9, metric).copy()
            
            # Combine data
            plot_data = pd.concat([other_data, vanuatu_data])
            
            # Sort by metric value
            plot_data = plot_data.sort_values(by=metric, ascending=info['inverse'])
            
            # Add user selected country if it exists
            if user_country and user_country in hpi_data['country'].values and user_country != 'Vanuatu':
                user_country_data = hpi_data[hpi_data['country'] == user_country].copy()
                plot_data = pd.concat([plot_data, user_country_data])
            
            col1, col2 = st.columns([2,1])
            
            with col1:
                st.write(f"**{info['description']}**")
                
                # Create custom color scale
                colors = ['#1B5E20', '#2E7D32', '#388E3C', '#43A047', '#4CAF50', 
                         '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9'] if info['inverse'] else \
                        ['#E8F5E9', '#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', 
                         '#4CAF50', '#43A047', '#388E3C', '#2E7D32', '#1B5E20']
                
                color_map = {country: colors[i] for i, country in enumerate(other_data['country'])}
                color_map['Vanuatu'] = '#9C27B0'  # Lavender purple for Vanuatu
                if user_country in color_map:
                    color_map[user_country] = '#FFA726'  # Orange for user country
                
                fig = px.bar(
                    plot_data,
                    x='country',
                    y=metric,
                    title=f'{"Lowest" if info["inverse"] else "Top"} 10 Countries by {metric}',
                    color='country',
                    color_discrete_map=color_map
                )
                
                fig.update_layout(
                    showlegend=False,
                    xaxis_tickangle=45,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("Rankings:")
                styled_df = plot_data[['country', metric]].reset_index(drop=True)
                
                # Style the dataframe to highlight Vanuatu
                def highlight_vanuatu(row):
                    color = '#F3E5F5' if row['country'] == 'Vanuatu' else ''
                    return ['background-color: {}'.format(color) for _ in row]
                
                styled_df = styled_df.style.apply(highlight_vanuatu, axis=1)
                st.dataframe(styled_df, hide_index=True, use_container_width=True)

# Geographic Distribution
st.header("1. Geographic Distribution of Educational Resources")
st.subheader("1.1 Provincial Overview")

col1, col2 = st.columns([2,1])
with col1:
    try:
        map_fig = create_map_visualization(
            data["Enrollment by School Type"], 
            'Total', 
            'Educational Institution Distribution'
        )
        if map_fig is not None:
            st.plotly_chart(map_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying map: {e}")

with col2:
    st.markdown("""
    **Analysis of Regional Distribution**
    
    The geographic distribution of educational institutions reveals:
    - [Placeholder for distribution pattern]
    - [Placeholder for regional disparities]
    - [Placeholder for access challenges]
    """)

# Enrollment Trends
st.header("2. Enrollment Patterns and Trends")
st.subheader("2.1 Overall Enrollment Statistics")

col1, col2 = st.columns([2,1])
with col1:
    enrollment_data = data["Enrollment by School Type"]
    enrollment_data = enrollment_data[enrollment_data['Province'].isin(PROVINCE_COLORS.keys())].copy()
    fig = px.sunburst(
        enrollment_data, 
        path=['Province'], 
        values='Total',
        color='Province',
        color_discrete_map=PROVINCE_COLORS,
        title="Total Enrollment Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    **Key Enrollment Insights**
    
    Analysis of enrollment data shows:
    - [Placeholder for enrollment trends]
    - [Placeholder for provincial comparisons]
    - [Placeholder for growth patterns]
    """)

# Gender Analysis
st.header("3. Gender Equity in Education")
st.subheader("3.1 Gender Distribution Analysis")

enrollment_details = data["Detailed Enrollment"]
col1, col2 = st.columns([2,1])
with col1:
    fig = create_gender_ratio_plot(enrollment_details, "enrollment")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    **Gender Equity Assessment**
    
    Current gender distribution indicates:
    - [Placeholder for gender ratio analysis]
    - [Placeholder for regional variations]
    - [Placeholder for improvement areas]
    """)

# Teacher Distribution
st.header("4. Teaching Resources")
st.subheader("4.1 Teacher Distribution and Qualifications")

teacher_data = data["Teachers Distribution"]
col1, col2 = st.columns([2,1])
with col1:
    fig = create_teacher_distribution(teacher_data)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    **Teaching Resource Analysis**
    
    The distribution of teaching resources shows:
    - [Placeholder for teacher allocation patterns]
    - [Placeholder for qualification levels]
    - [Placeholder for resource gaps]
    """)

# Age Distribution Analysis
st.header("5. Age Distribution and Educational Access")
st.subheader("5.1 Age-based Enrollment Patterns")

age_data = data["Age Distribution"]
col1, col2 = st.columns([3,1])
with col1:
    fig = create_age_distribution_analysis(age_data) 
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20)) # Added space around the plot
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    **Age Distribution Insights**
    
    Analysis of age-based enrollment reveals:
    - Early childhood enrollment (under 3) varies significantly by province
    - Core age groups (3-4 years) show highest enrollment rates
    - Over-age enrollment (>6 years) indicates potential access issues
    - Year-over-year trends show changing enrollment patterns
    
    **Key Findings:**
    - Most provinces show peak enrollment in 3-4 age group
    - Rural provinces have higher rates of over-age enrollment
    - Urban areas show more consistent age distributions
    """)

# Recommendations
st.header("6. Recommendations and Future Directions")
st.markdown("""
Based on the comprehensive analysis presented in this report, we recommend the following actions:

1. **Short-term Recommendations**
   - [Placeholder for immediate action items]
   - [Placeholder for quick wins]

2. **Medium-term Strategies**
   - [Placeholder for 1-3 year goals]
   - [Placeholder for development plans]

3. **Long-term Vision**
   - [Placeholder for 5+ year objectives]
   - [Placeholder for systemic changes]
""")

# Methodology and Data Sources
st.header("7. Methodology and Data Sources")
st.markdown("""
This report utilizes data from the following sources:
- Vanuatu Ministry of Education
- [Placeholder for additional sources]

**Methodology:**
- [Placeholder for data collection methods]
- [Placeholder for analysis approach]
- [Placeholder for limitations]
""")

# Footer
st.markdown("---")
st.markdown("""
*Report prepared using data from the Vanuatu Ministry of Education*  
Last updated: 2023
""")
