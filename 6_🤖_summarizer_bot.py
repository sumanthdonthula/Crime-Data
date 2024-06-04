from openai import OpenAI
import pandas as pd

import streamlit as st
import json

st.title("🐼 PandaBot")
st.write("👋 Hey I am a Content Summarizing Bot, I highlight key points about our Data")

@st.cache_data
def get_data():
    crime_data = pd.read_csv('crime_data.csv')
    data=json.dumps(crime_data.to_dict(orient="records"))

    return data


st.button("Reset", type="primary")
if st.button("Summarize"):
    client = OpenAI(api_key="")

    data = get_data()
    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Summarize and Highlight key incidents from the data{data}"}],
    stream=True,)

    completion_string = ""
    
    for response in stream:
        if response.choices[0].delta.content!=None:
            completion_string += response.choices[0].delta.content

    st.write(completion_string)


