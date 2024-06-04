import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="% of the Selected Problem per month", page_icon="📊")

st.markdown("**% of the Selected Problem per month**")
st.sidebar.header("% of the Selected Problem per month")
st.write("This Plot represents the % share of the problem per month over months")

@st.cache_data
def get_data():
    crime_data = pd.read_csv('crime_data.csv')
    df = crime_data
    df['Response_Date'] = pd.to_datetime(df['Response_Date'])
    df['Year']=df['Response_Date'].dt.year

    return df

def get_monthly_percent_data(data_frame):
    yearly_df=data_frame[data_frame['Year']==Year]
        
    yearly_df_law_enf=yearly_df[(yearly_df['Year'] == Year) & (yearly_df['Agency_Type'] == 'Law Enforcement')]
                
    #filtered_df =yearly_df_law_enf[(yearly_df_law_enf['Response_Date'].dt.month==month_to_num[Month])]
    filtered_df=yearly_df_law_enf

    filtered_df['Month_Number']=filtered_df['Response_Date'].dt.month
    
    
    problem_count_df = filtered_df.groupby(['Month_Number','Problem']).size().reset_index(name='Count')
    
    problem_count_df['Month_Number']=problem_count_df['Month_Number'].astype(int)
    problem_count_df['Month']=problem_count_df['Month_Number'].map(lambda x: month_to_num[x] )

    problem_count_df=problem_count_df.sort_values(by=['Month_Number'])

    grouped = problem_count_df.groupby('Month')['Count'].sum()        

    # Group by 'date' and sum the counts for each type
    
    # Calculate percentage of each type by total count for each date
    problem_count_df['percentage'] = problem_count_df.apply(lambda x: (x['Count'] / grouped[x['Month']]) * 100, axis=1)
    problem_count_df['Month_Count'] = problem_count_df.apply(lambda x: grouped[x['Month']], axis=1)
    
    return problem_count_df[problem_count_df['Problem']==Problem]
    
def plot_monthly_percentage_data(final_df):
    final_df=get_monthly_percent_data(data_frame)
    line_fig = px.line(final_df, x='Month', y='percentage',text='Count')
    line_fig.update_traces(textposition="bottom left")
    
    return line_fig

try:
    data_frame = get_data()
    
    grouped_df = data_frame.groupby(['Problem']).size().reset_index(name='Count')
        
    top_10_counts=grouped_df.nlargest(10, 'Count')
    
    month_to_num = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    unique_month_names = list(month_to_num.keys())
    
    Year= st.selectbox(
        "Choose Year", list(data_frame['Response_Date'].dt.year.unique())
    )
    
    Problem = st.selectbox(
        "Choose Problem", list(top_10_counts['Problem'])
    )
    
    if not Year:
        st.error("Please select at least one Year.")
    else:
        final_df=get_monthly_percent_data(data_frame)
        line_fig=plot_monthly_percentage_data(final_df)
        st.plotly_chart(line_fig)
        
        
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
