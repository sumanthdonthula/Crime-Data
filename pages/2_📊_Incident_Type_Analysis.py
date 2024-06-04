import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_title="Distribution of Problems per Incident Type", page_icon="📊")
st.sidebar.header("Distribution of Problems per Incident Type")

@st.cache_data
def get_data():
    crime_data = pd.read_csv('crime_data.csv')
    df = crime_data
    df['Response_Date'] = pd.to_datetime(df['Response_Date'])
    df['Year']=df['Response_Date'].dt.year

    return df

def get_problems_per_incident(data_frame, Year):
    data_frame=data_frame[data_frame['Year']==Year]
    problems = data_frame[data_frame['Incident_Type'].isin([incident_type])]
    
    return problems.groupby(['Incident_Type', 'Problem']).size().reset_index(name='Count')
 
def plot_problems_per_incident(grouped_df):
    fig = px.bar(grouped_df, x='Problem', y='Count',text='Count')
    # Update the layout for better visibility of labels
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    
    return fig
    


try:
    data_frame = get_data()
    
    Year = st.selectbox(
        "Choose Year", list(data_frame['Response_Date'].dt.year.unique())
    )
    
    
    incident_type = st.selectbox(
        "Choose Type of Incident",sorted(list(data_frame[(data_frame['Year'] == Year) & (data_frame['Agency_Type'] == 'Law Enforcement')]['Incident_Type'].unique()))
)
    
    if not Year and incident_type:
        st.error("Please select at least one Year and incident type")
    else:
        
        
        grouped_df = get_problems_per_incident(data_frame, Year)
        fig=plot_problems_per_incident(grouped_df)
        st.markdown("**Distribution of Problems per Incident Type over an Year**")
        title='Histogram of '+ str(incident_type)+' problems'
        st.write(title)

        
        # Display the bar chart in Streamlit
        st.plotly_chart(fig)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
