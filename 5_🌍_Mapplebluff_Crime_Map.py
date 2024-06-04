import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

st.set_page_config(page_title="Mapple Bluff Map with Crime Frequency by Place", page_icon="🌍")

st.markdown("**Mapple Bluff Crime Map**")
st.sidebar.header("Mapple Bluff Map with Crime Frequency by Place")
st.write(
    """This Map Shows the Frequency of Incidents over Year per place (Lattitude and Longitude)"""
)

@st.cache_data
def get_data():
    crime_data = pd.read_csv('crime_data.csv')
    data_frame = crime_data
    data_frame['Response_Date'] = pd.to_datetime(data_frame['Response_Date'])
    data_frame['Year']=data_frame['Response_Date'].dt.year

    return data_frame
    
# Define a function to assign colors based on count
def assign_color(count):
    if count >= 100:
        return 'purple'
    elif count >= 50:
        return 'orange'
    elif count>25 and count<=50:
        return 'green'
        
def plot_map(data_frame):
    data_frame=data_frame[(data_frame["Latitude"]!='unknown') & (data_frame["Longitude"]!='unknown')]
    data_frame=data_frame[data_frame['Year']==Year]
    
    data_frame["Latitude"] = pd.to_numeric(data_frame["Latitude"])
    data_frame["Longitude"] = pd.to_numeric(data_frame["Longitude"])
    
    
    m = folium.Map(data_frame[['Latitude', 'Longitude']].mean().values.tolist())

    counts = data_frame.groupby(['Latitude','Longitude']).size().reset_index(name='Count')
    
    

    # Loop through each ZIP code and count
    for index, row in counts.iterrows():
    
        lat = row['Latitude']
        long = row['Longitude']
        count = row['Count']
        # Check if location was found
        if lat and long:
            # Assign color based on count
            color = assign_color(count)
            # Add a marker for the ZIP code with assigned color
            folium.Marker([lat, long],
            popup=folium.Popup(str(int(count))),
            html=str(int(count)),
            icon=folium.Icon(color=color)

    ).add_to(m)
            
    
        else:
            st.write(f"Location not found for lat long")
            
    return m


try:
    
    # Create a map
    
    data_frame=get_data()
    
    Year = st.selectbox(
        "Choose Year", list(data_frame['Response_Date'].dt.year.unique())
    )
    
    map_plt=plot_map(data_frame)
    st_folium(map_plt, height=540,width=540, returned_objects=[])
    
    st.write("**Color Mapping**")
    st.write("🟣(# of Incidents >= 100)")
    st.write("🟠(50 >= # of Incidents < 100)")
    st.write("🟢(25 >=# of Incidents < 50)")
    st.write("🔵(# of Incidents < 25)")

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )