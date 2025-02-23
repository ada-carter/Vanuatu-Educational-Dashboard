import pandas as pd 
import plotly.express as px
import streamlit as st

def preprocess_data(data):
    """
    We need to preprocess the CSV so that it is unstacked
    The raw data from the MoE is stacked, so we should preserve it.
    Preprocess the CSV so that:
      - Rows with an overall province total (i.e. not "F", "M", or "Grand Total") are marked as 'Overall'
      - Gender rows (where Province is "F" or "M") inherit the province name from the previous overall row.
    """
    # Create a new column that will hold the true province name
    data['Province_Name'] = data['Province'].where(~data['Province'].isin(['F', 'M', 'Grand Total']))
    data['Province_Name'] = data['Province_Name'].ffill()

    # Create a Gender column: if the Province cell is "F" or "M", that's the gender; otherwise, mark it as 'Overall'
    data['Gender'] = data['Province'].apply(lambda x: x if x in ['F','M'] else 'Overall')
    return data

def create_enrollment_summary(data):
    """Creates a summary table of overall enrollment data."""
    overall = data[data['Gender'] == 'Overall']
    summary = overall.groupby('Province_Name')[['PreSchool_Total', 'Primary_Total', 'Secondary_Total', 'Total']].sum().reset_index()
    summary.rename(columns={'Province_Name': 'Province'}, inplace=True)
    return summary

def create_gender_enrollment_summary(data):
    """Creates a summary table of enrollment data by gender."""
    gender_data = data[data['Gender'].isin(['F', 'M'])].copy()
    gender_summary = gender_data.groupby(['Province_Name', 'Gender'])[['PreSchool_Total', 'Primary_Total', 'Secondary_Total', 'Total']].sum().reset_index()
    gender_summary.rename(columns={'Province_Name': 'Province'}, inplace=True)
    return gender_summary

def create_enrollment_by_grade(data):
    """Creates a DataFrame of enrollment by grade using overall rows."""
    grade_cols = ['Grade_1', 'Grade_2', 'Grade_3', 'Grade_4', 'Grade_5', 'Grade_6', 
                  'Grade_7', 'Grade_8', 'Grade_9', 'Grade_10', 'Grade_11', 'Grade_12', 
                  'Grade_13', 'Grade_14']
    overall = data[data['Gender'] == 'Overall']
    enrollment_by_grade = overall.groupby('Province_Name')[grade_cols].sum().reset_index()
    enrollment_by_grade.rename(columns={'Province_Name': 'Province'}, inplace=True)
    return enrollment_by_grade

def create_total_enrollment_bar_chart(data):
    """Creates a bar chart of total enrollment by province."""
    summary = create_enrollment_summary(data)
    fig = px.bar(summary, x='Province', y='Total', title='Total Enrollment by Province',
                 color='Province', color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(showlegend=False)
    return fig

def create_enrollment_type_pie_chart(data):
    """Creates a pie chart of enrollment by education level (PreSchool, Primary, Secondary)."""
    summary = create_enrollment_summary(data)
    melted_summary = pd.melt(summary, id_vars=['Province'], 
                             value_vars=['PreSchool_Total', 'Primary_Total', 'Secondary_Total'],
                             var_name='Education Level', value_name='Enrollment')
    fig = px.pie(melted_summary, values='Enrollment', names='Education Level', 
                 title='Enrollment by Education Level', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=True)
    return fig

def create_gender_distribution_bar_chart(data):
    """Creates a grouped bar chart of enrollment by gender and province."""
    gender_summary = create_gender_enrollment_summary(data)
    fig = px.bar(gender_summary, x='Province', y=['PreSchool_Total', 'Primary_Total', 'Secondary_Total'],
                 title='Enrollment by Gender and Education Level', barmode='group',
                 color='Gender', color_discrete_map={'F': '#FFB6C1', 'M': '#ADD8E6'})
    fig.update_layout(yaxis_title='Enrollment', legend_title='Gender')
    return fig

def create_grade_enrollment_line_chart(data):
    """Creates a line chart of enrollment by grade."""
    enrollment_by_grade = create_enrollment_by_grade(data)
    grade_cols = ['Grade_1', 'Grade_2', 'Grade_3', 'Grade_4', 'Grade_5', 'Grade_6', 
                  'Grade_7', 'Grade_8', 'Grade_9', 'Grade_10', 'Grade_11', 'Grade_12', 
                  'Grade_13', 'Grade_14']
    melted_grades = pd.melt(enrollment_by_grade, id_vars=['Province'], 
                            value_vars=grade_cols, var_name='Grade', value_name='Enrollment')
    fig = px.line(melted_grades, x='Grade', y='Enrollment', color='Province',
                  title='Enrollment Trend by Grade', color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.update_layout(yaxis_title='Enrollment', legend_title='Province')
    return fig

def create_total_vs_secondary_scatter(data):
    """Creates a scatter plot of Total vs Secondary Enrollment by Province."""
    summary = create_enrollment_summary(data)
    fig = px.scatter(summary, x='Total', y='Secondary_Total', color='Province', hover_data=['Province'],
                     title='Total Enrollment vs Secondary Enrollment by Province',
                     color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(xaxis_title='Total Enrollment', yaxis_title='Secondary Enrollment', showlegend=False)
    return fig