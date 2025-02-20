import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
from visualizations import (create_enrollment_trend, create_teacher_distribution,
                          create_gender_ratio_plot, create_enrollment_heatmap,
                          create_percentage_plot)

# Page configuration
st.set_page_config(layout="wide", page_title="Vanuatu Education Dashboard")

# Load data
try:
    data = load_data("VData.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
st.sidebar.title("Navigation")
section = st.sidebar.radio("Select Section", 
    ["Overview",
     "NER Analysis",
     "Enrollment Analysis",
     "Teacher Distribution",
     "Age Distribution"])

# Main content
st.title("Vanuatu Educational Dashboard")

if section == "Overview":
    st.header("Education System Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Enrollment by School Type")
        enrollment_data = data["Enrollment by School Type"]
        # Fix: Use ECCE column for values instead of Total
        fig = px.pie(enrollment_data, values='ECCE', names='School_Type')
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Teacher Distribution")
        teacher_data = data["Teachers Distribution"]
        # Fix: Show total teachers by province
        teacher_summary = teacher_data.groupby('Province')['Total'].sum().reset_index()
        fig = px.bar(teacher_summary, x='Province', y='Total', title='Total Teachers by Province')
        st.plotly_chart(fig)

elif section == "NER Analysis":
    st.header("Net Enrollment Rate (NER) Analysis")
    ner_data = data["NER for ECCE"]
    
    # Trend analysis
    st.subheader("NER Trends (2018-2020)")
    fig = create_percentage_plot(ner_data, 
                               ['Female_2018', 'Male_2018', 'Total_2018',
                                'Female_2019', 'Male_2019', 'Total_2019',
                                'Female_2020', 'Male_2020', 'Total_2020'])
    st.plotly_chart(fig)

elif section == "Enrollment Analysis":
    st.header("Enrollment Analysis")
    enrollment_data = data["Detailed Enrollment"]
    
    # Enrollment heatmap
    st.subheader("Enrollment Distribution")
    fig = create_enrollment_heatmap(enrollment_data)
    st.plotly_chart(fig)
    
    # Gender distribution
    st.subheader("Gender Distribution")
    fig = create_gender_ratio_plot(enrollment_data)
    st.plotly_chart(fig)

elif section == "Teacher Distribution":
    st.header("Teacher Distribution Analysis")
    teacher_data = data["Teachers Distribution"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Teachers by Province")
        fig = create_teacher_distribution(teacher_data)
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Gender Distribution of Teachers")
        fig = create_gender_ratio_plot(teacher_data)
        st.plotly_chart(fig)

elif section == "Age Distribution":
    st.header("Age Distribution Analysis")
    age_data = data["Age Distribution"]
    
    st.subheader("Enrollment Trends by Age")
    fig = create_enrollment_trend(age_data)
    st.plotly_chart(fig)

# Footer
st.markdown("---")
st.markdown("Data source: Vanuatu Ministry of Education")
