import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analysis of Top 10 Problems by Year", page_icon="📊")


@st.cache_data
def get_data():
    crime_data = pd.read_csv('crime_data.csv')
    df = crime_data
    df['Response_Date'] = pd.to_datetime(df['Response_Date'])
    df['Year']=df['Response_Date'].dt.year

    return df
    
def get_top_10_problem_data(data_frame):
    data_frame=data_frame[data_frame['Year']==Year]
    grouped_df = data_frame.groupby(['Problem']).size().reset_index(name='Count')
    
    return grouped_df.nlargest(10, 'Count')

def plot_top_10_problem_data(top_10_counts):
    # Plot histogram        
    fig = px.bar(top_10_counts, x='Problem', y='Count', text='Count')
    # Update the layout for better visibility of labels
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    
    return fig
    


try:
    data_frame = get_data()
    
    Year = st.selectbox(
        "Choose Year", list(data_frame['Response_Date'].dt.year.unique())
    )
    
    
    if not Year:
        st.error("Please select at least one Year and incident type")
    else:
        
        top_10_counts=get_top_10_problem_data(data_frame)

        st.markdown("**Counts of Top 10 Problems over Year**")
        st.write("This table represents the number of top 10 Problems over Year")

        title='Histogram of problems'
        st.write(top_10_counts.sort_values(by='Count', ascending=False))
        
        st.markdown("**Analysis of Top 10 Problems by Year**")
        st.write("This Plot represent Distribution of Top 10 Problems over an Year")
        
        fig=plot_top_10_problem_data(top_10_counts)
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