import streamlit as st
import pandas as pd
import plotly.express as px
import os
from data_loader import load_data
from visualizations import *
from detailed_enrollment_visualizations import *  # Import the new script
import plotly.graph_objects as go
import json

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
    
    available_countries = sorted(hpi_data['country'].unique().tolist())
    default_country = "United States" if "United States" in available_countries else available_countries[0]
    user_country = st.selectbox("Select a country for comparison:", available_countries, 
                               index=available_countries.index(default_country))
    
    metric_tabs = st.tabs(list(metrics.keys()))
    
    for i, (metric, info) in enumerate(metrics.items()):
        with metric_tabs[i]:
            metric_data = hpi_data.copy().dropna(subset=[metric])
            
            # Format numbers for display
            if metric == 'HPI':
                metric_data[metric] = metric_data[metric].apply(lambda x: float(f"{x:.1f}"))
            
            metric_data['ranking'] = metric_data[metric].rank(ascending=info['inverse'], method='min').astype(int)
            
            # Get reference data
            vanuatu_data = metric_data[metric_data['country'] == 'Vanuatu'].copy()
            user_country_data = metric_data[metric_data['country'] == user_country].copy()
            other_data = metric_data[~metric_data['country'].isin(['Vanuatu', user_country])]
            
            total_countries = len(metric_data)
            vanuatu_rank = int(vanuatu_data['ranking'].iloc[0]) if not vanuatu_data.empty else "N/A"
            user_country_rank = int(user_country_data['ranking'].iloc[0]) if not user_country_data.empty else "N/A"
            
            col1, col2 = st.columns([2,1])
            
            with col1:
                st.write(f"**{info['description']}**")
                if vanuatu_rank != "N/A":
                    st.write(f"Vanuatu ranks **{vanuatu_rank}** out of {total_countries} countries")
                if user_country_rank != "N/A":
                    st.write(f"{user_country} ranks **{user_country_rank}** out of {total_countries} countries")
                
                # Get top/bottom 10 countries
                if info['inverse']:
                    plot_data = other_data.nsmallest(10, metric).copy()
                else:
                    plot_data = other_data.nlargest(10, metric).copy()
                
                # Always include Vanuatu and selected country
                for special_data in [vanuatu_data, user_country_data]:
                    if not special_data.empty:
                        plot_data = pd.concat([plot_data, special_data])
                
                # Sort the data
                plot_data = plot_data.sort_values(metric, ascending=info['inverse'])
                
                # Create the visualization
                color_scale = px.colors.sequential.YlGn_r if info['inverse'] else px.colors.sequential.YlGn
                fig = px.bar(
                    plot_data,
                    x='country',
                    y=metric,
                    title=f'{"Lowest" if info["inverse"] else "Highest"} Values for {metric}',
                    color=metric,
                    color_continuous_scale=color_scale
                )
                
                fig.update_layout(
                    showlegend=False,
                    xaxis=dict(
                        tickangle=45,
                        tickmode='array',
                        tickvals=plot_data['country'],
                        ticktext=[f'<b>{c}</b>' if c in ['Vanuatu', user_country] else c 
                                for c in plot_data['country']]
                    ),
                    height=500,
                    margin=dict(b=100)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("Rankings (sorted by performance):")
                
                # Prepare dataset for display
                display_data = metric_data[['country', metric, 'ranking']].copy()
                # Format numbers based on metric type
                if metric == 'HPI':
                    display_data[metric] = display_data[metric].apply(lambda x: '{:.1f}'.format(float(x)))
                else:
                    display_data[metric] = display_data[metric].apply(lambda x: '{:.2f}'.format(float(x)))
                
                display_data['ranking'] = display_data['ranking'].astype(int)
                display_data = display_data.sort_values('ranking')
                
                # Calculate Vanuatu's row number
                vanuatu_idx = display_data.index[display_data['country'] == 'Vanuatu'].tolist()[0]
                
                def highlight_countries(row):
                    color = ''
                    if row['country'] == 'Vanuatu':
                        color = 'background-color: #F3E5F5'
                    elif row['country'] == user_country:
                        color = 'background-color: #FFF3E0'
                    return [color] * len(row)
                
                # Style the dataframe
                styled_df = display_data.style.apply(highlight_countries, axis=1)
                
                # Display scrollable dataframe with scroll position set to Vanuatu
                element = st.dataframe(
                    styled_df,
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )
                
                # Use JavaScript to scroll to Vanuatu's position
                row_height = 35  # Approximate height of each row in pixels
                scroll_position = max(0, (vanuatu_idx * row_height) - 200)  # Center Vanuatu in view
                st.markdown(
                    f"""
                    <script>
                        const element = document.querySelector('.stDataFrame div[data-testid="stDataFrame"] div');
                        element.scrollTop = {scroll_position};
                    </script>
                    """,
                    unsafe_allow_html=True
                )
                
                # Add note about scrolling
                st.caption("Table automatically scrolls to Vanuatu's position. Vanuatu and selected country are highlighted.")

# Population Trends Section
st.header("Population Trends")
try:
    population_data = pd.read_csv("data/Population.csv")
    
    # Add toggle for school-age only view
    school_age_only = st.checkbox("Show only school-age population (0-19 years)", value=True)
    
    col1, col2 = st.columns([2,1])
    with col1:
        pop_fig = create_population_trend_visualization(population_data, school_age_only)
        st.plotly_chart(pop_fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        **Population Growth Analysis**
        
        The population trends show:
        - Consistent growth across age groups
        - School-age population (0-19) forms a significant demographic
        - Notable expansion in youth population
        - Growing demand for educational resources
        """)
        
        # Calculate and display key statistics
        total_growth = (population_data['Total Population'].iloc[-1] / population_data['Total Population'].iloc[0] - 1) * 100
        school_age_pop = population_data[['0--4', '5--9', '10--14', '15--19']].sum(axis=1).iloc[-1]
        school_age_percent = (school_age_pop / population_data['Total Population'].iloc[-1]) * 100
        
        latest_year = population_data['Year'].max()
        st.markdown(f"""
        **Key Statistics ({latest_year}):**
        - Total Population: {population_data['Total Population'].iloc[-1]:,.0f}
        - School-age Population (0-19): {school_age_pop:,.0f}
        - School-age percentage: {school_age_percent:.1f}%
        - Population growth (2009-2020): {total_growth:.1f}%
        """)

except Exception as e:
    st.error(f"Error loading population data: {e}")

# New Province Data Visualizations Section
st.header("Province Data Visualizations")

try:
    # Load detailed enrollment data
    detailed_enrollment = data["Detailed Enrollment"]
    detailed_enrollment = preprocess_data(detailed_enrollment)

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Total Enrollment", "Enrollment by Level", "Gender Distribution", "Grade Trends", "Total vs Secondary"
    ])

    with tab1:
        # Total Enrollment by Province
        fig1 = create_total_enrollment_bar_chart(detailed_enrollment)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        # Enrollment by Education Level
        fig2 = create_enrollment_type_pie_chart(detailed_enrollment)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        # Gender Distribution by Education Level
        fig3 = create_gender_distribution_bar_chart(detailed_enrollment)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        # Enrollment Trend by Grade
        fig4 = create_grade_enrollment_line_chart(detailed_enrollment)
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)

    with tab5:
        # Total vs Secondary Enrollment
        fig5 = create_total_vs_secondary_scatter(detailed_enrollment)
        if fig5:
            st.plotly_chart(fig5, use_container_width=True)

except Exception as e:
    st.error(f"Error in Province Data Visualizations: {e}")


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
