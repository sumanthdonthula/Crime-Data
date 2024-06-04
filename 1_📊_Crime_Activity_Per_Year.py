import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analysis of Crime Activity by Year ", page_icon="📊")
st.sidebar.header("Analysis of Crime Activity by Year")

@st.cache_data
def get_data():
    crime_data = pd.read_csv('crime_data.csv')
    df = crime_data
    df['Response_Date'] = pd.to_datetime(df['Response_Date'])
    df['Year']=df['Response_Date'].dt.year

    return df
    
def get_yearly_df(data_frame, Year):
    return data_frame[data_frame['Year']==Year]
    
def get_yearly_law_enf_df(yearly_df, Year):
    return yearly_df[(yearly_df['Year'] == Year) & (yearly_df['Agency_Type'] == 'Law Enforcement')]

def get_daily_incidents_data(yearly_df_law_enf):
    # Group by 'Date' column and count the number of records per day
    records_per_day = yearly_df_law_enf.groupby('Response_Date').size().reset_index(name='Count')        
    records_per_day['Year']=records_per_day['Response_Date'].dt.year
    records_per_day=records_per_day.set_index("Year")
    return records_per_day.loc[Year]

def plot_incidents_per_year(daily_data):
    line_fig = px.line(daily_data, x='Response_Date', y='Count',text='Count')
    line_fig.update_traces(textposition="top center")
    return line_fig
    
    
def get_agency_type_data(yearly_df):
    # Group by 'Agency Type' column and count the number of records per day
    return yearly_df['Agency_Type'].value_counts()

def plot_agency_type_data(Agency_Type):
    fig1 = px.pie(Agency_Type, names=Agency_Type.index, height=540, width=540, values='count')
    fig1.update_traces(textposition='inside')
    fig1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig1
    
def get_incident_type_data(yearly_df_law_enf):
    # Group by 'Agency Type' column and count the number of records per day
    return yearly_df_law_enf['Incident_Type'].value_counts()

def plot_incident_type_data(incident_type):
    fig2 = px.pie(incident_type, names=incident_type.index, height=540, width=540, values='count')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig2
    
def get_city_type_data(yearly_df_law_enf):
    # Group by 'Agency Type' column and count the number of records per day
    return yearly_df_law_enf['Place Name Census'].value_counts()

def plot_city_type_data(incident_type):
    fig3 = px.pie(city_counts, names=city_counts.index, height=540, width=540, values='count')
    fig3.update_traces(textposition='inside')
    fig3.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig3

    
try:
    data_frame = get_data()
    
    Year = st.selectbox(
        "Choose Year", list(data_frame['Response_Date'].dt.year.unique())
    )
    if not Year:
        st.error("Please select at least one Year.")
    else:
        
        yearly_df= get_yearly_df(data_frame, Year)       
        yearly_df_law_enf=get_yearly_law_enf_df(yearly_df, Year)
        
        daily_data=get_daily_incidents_data(yearly_df_law_enf)
        
        st.markdown("**Analysis of Crime Activity by Year**")
        st.write("This Plot represent the total number of Crime Incidents reported per Day over an Year")
        
        line_fig=plot_incidents_per_year(daily_data)
        st.plotly_chart(line_fig)
        
        st.markdown("**Pie Chart, proportions of EMS Fire vs Law Enforcement**")
        st.write("This chart represents EMS Fire vs Law Enforcement Incidents over an Year")
        
        Agency_Type = get_agency_type_data(yearly_df)
        fig1 = plot_agency_type_data(Agency_Type)
        
        st.plotly_chart(fig1)
               
        incident_type = get_incident_type_data(yearly_df_law_enf)
        fig2=plot_incident_type_data(incident_type)
        
        st.markdown("**Pie Chart, proportion of Incidents by Incident Type**")
        st.write("This chart represents proportion of Incidents per Incident over an Year")
        st.plotly_chart(fig2)
        
        city_counts = get_city_type_data(yearly_df_law_enf)
        fig3=plot_city_type_data(city_counts)
        
        st.markdown("**Pie Chart, proportion of Incidents by City**")
        st.write("This chart represents proportion of Incidents per City over an Year")
        
        st.plotly_chart(fig3)
        
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )

