# Get the list of URLs and its corresponding label
import os
import requests
import pandas as pd
import streamlit as st
from decouple import config

if "API_ENDPOINT" not in os.environ:
    os.environ["API_ENDPOINT"] = config("API_ENDPOINT")


def fetch_labels():
    url = os.environ["API_ENDPOINT"] + "/labels"
    response = requests.request("GET", url)
    return response.json()


st.set_page_config(page_title='LinkScribe', page_icon=':globe_with_meridians:', layout='wide')

st.sidebar.title("Options")

st.header('LinkScribe')
st.subheader('List of websites')

st.write("Here, you can find a list of the websites you classified above.")

labels = fetch_labels()
df = pd.DataFrame(labels)
st.table(df)
