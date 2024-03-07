from numpy import *
import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparison SSG-SEA input/output",page_icon=":books:",layout="wide")

st.title(":books: Comparison SSG-SEA input/output Preliminary Study")

file = "SBS_UG_new.xlsx"

df_lean = pd.read_excel(file,sheet_name="Skill_SSG_Data")
df_all = pd.read_excel(file,sheet_name="Skill_SSG_All")
df_diff = pd.read_excel(file,sheet_name="Skill_SSG_Diff")
df_data = pd.read_excel(file,sheet_name="Course_Data")

columns = ['id', 'skill', 'skill_type']

courses = df_lean['id'].unique()
st.sidebar.header("Customization")

with st.sidebar:
    st.write("This dashboard is to facilitate visualization of data collected\
             from skills tagging using SkillsFuture Skills Extraction Algorithm.\
             This preliminary study is done for SBS UG courses only.")
    
    selected_courses = st.multiselect('Select courses (all courses selected by default):', courses, default=[])
    
    st.write('---')
    st.write("skill_type legend")
    st.write("**TSC:** Technical Skills and Competencies")
    st.write("**CCS:** Critical Core Skills")
    
if len(selected_courses) == 0:
    selected_courses = courses

st.header("General distribution of :green[all courses]")
col1,col2 = st.columns((2))

st.header("Overview of :orange[user selected courses]")
col3,col4,col5 = st.columns((3))

filtered_df_lean = df_lean[df_lean['id'].isin(selected_courses)]
filtered_df_all = df_all[df_all['id'].isin(selected_courses)]
filtered_df_diff = df_diff[df_diff['id'].isin(selected_courses)]

filtered_df_lean = filtered_df_lean[columns]
filtered_df_all = filtered_df_all[columns]
filtered_df_diff = filtered_df_diff[columns]

skill_counts_diff = filtered_df_diff['skill_type'].value_counts()

N_lean = len(filtered_df_lean)
N_all = len(filtered_df_all)
N_diff = len(filtered_df_diff)

input_columns = ['id', 'lean', 'all']
filtered_df_data = df_data[df_data['id'].isin(selected_courses)]
filtered_df_data = filtered_df_data[input_columns]

with col1:
    st.write("Number of *skill_types* picked up by SSG_SEA for Course Aims + Course ILOs + Course Content")
    fig = px.histogram(df_lean, x="skill_type")#,color="id")
    fig.update_layout(yaxis_range=[0,300])
    st.plotly_chart(fig,use_container_width=True,height=400)

with col2:
    st.write("Number of *skill_types* picked up by SSG_SEA for entire OBTL less sensitive data and Graduate Attributes")
    fig = px.histogram(df_all, x="skill_type")#,color="id")
    fig.update_layout(yaxis_range=[0,300])
    st.plotly_chart(fig,use_container_width=True,height=400)

with col3:
    st.subheader("Number of skills tagged: "+str(N_lean))
    st.write("List of skills picked up by SSG_SEA for Course Aims + Course ILOs + Course Content")
    st.dataframe(filtered_df_lean, use_container_width=True, hide_index=True)

with col4:
    st.subheader("Number of skills tagged: "+str(N_all))
    st.write("List of skills picked up by SSG_SEA for entire OBTL less sensitive data and Graduate Attributes")
    st.dataframe(filtered_df_all, use_container_width=True, hide_index=True)

with col5:
    st.subheader("Distribution of *skill_type* (Additional skills: "+str(N_diff)+")")
    fig = px.pie(skill_counts_diff, values=skill_counts_diff.values, names=skill_counts_diff.index)
    st.plotly_chart(fig,use_container_width=True,height=400)

st.subheader("Data inputs")
st.dataframe(filtered_df_data, use_container_width=True, hide_index=True)
