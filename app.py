import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
from visualizations import (create_enrollment_trend, create_teacher_distribution,
                            create_gender_ratio_plot, create_enrollment_heatmap,
                            create_percentage_plot)

# Page configuration
st.set_page_config(layout="wide", page_title="Vanuatu Education Dashboard")

# Load data from individual CSV files in the data folder
try:
    data = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Use tabs for navigation
tabs = st.tabs(["Overview", "NER Analysis", "Enrollment Analysis", "Teacher Distribution", "Age Distribution"])

with tabs[0]:
    st.header("Education System Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Enrollment by School Type")
        enrollment_data = data["Enrollment by School Type"]
        # Use ECCE column for pie values
        fig = px.pie(enrollment_data, values='ECCE', names='School_Type')
        st.plotly_chart(fig)
    with col2:
        st.subheader("Teacher Distribution")
        teacher_data = data["Teachers Distribution"]
        teacher_summary = teacher_data.groupby('Province')['Total'].sum().reset_index()
        fig = px.bar(teacher_summary, x='Province', y='Total', title='Total Teachers by Province')
        st.plotly_chart(fig)

with tabs[1]:
    st.header("Net Enrollment Rate (NER) Analysis")
    ner_data = data["NER for ECCE"]
    st.subheader("NER Trends (2018-2020)")
    fig = create_percentage_plot(ner_data, 
                                 ['Female_2018', 'Male_2018', 'Total_2018',
                                  'Female_2019', 'Male_2019', 'Total_2019',
                                  'Female_2020', 'Male_2020', 'Total_2020'])
    st.plotly_chart(fig)

with tabs[2]:
    st.header("Enrollment Analysis")
    enrollment_details = data["Detailed Enrollment"]
    st.subheader("Enrollment Distribution")
    fig = create_enrollment_heatmap(enrollment_details)
    st.plotly_chart(fig)
    st.subheader("Gender Distribution")
    fig = create_gender_ratio_plot(enrollment_details)
    st.plotly_chart(fig)

with tabs[3]:
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

with tabs[4]:
    st.header("Age Distribution Analysis")
    age_data = data["Age Distribution"]
    st.subheader("Enrollment Trends by Age")
    fig = create_enrollment_trend(age_data)
    st.plotly_chart(fig)

st.markdown("---")
st.markdown("Data source: Vanuatu Ministry of Education")
