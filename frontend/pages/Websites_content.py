import os
import json
import time
import requests
import streamlit as st
from decouple import config
import streamlit.components.v1 as components

# set the api endpoint
if "API_ENDPOINT" not in os.environ:
    os.environ["API_ENDPOINT"] = config("API_ENDPOINT")


def call_api(input_url):
    # call the api
    payload = json.dumps([{"url": input_url}])
    headers = {"Content-Type": "application/json"}
    url = os.environ["API_ENDPOINT"] + "/website/content"
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()
    return results


st.set_page_config(page_title='LinkScribe', page_icon=':globe_with_meridians:', layout='wide')

st.sidebar.title("Options")

st.header('LinkScribe')
st.subheader('Website Content 💻')

st.write("Here, you can find the summary of the content of the website you classified above.")

with st.expander("Website URL", expanded=True):
    st.write("The website is: ", st.session_state['url'])

tab1, tab2, tab3, tab4 = st.tabs(["Title", "Class", "Summary", "Preview"])
title = call_api(st.session_state['url'])
# title, summary = call_api(st.session_state['url'])

with tab1:
    st.write(f'The website title is: {title}.')

with tab2:
    st.write(f"The website was classified as {st.session_state['results']}.")

with tab3:
    st.write("Summary: ")

with tab4:
    st.write("Preview: ")
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)

    components.iframe(st.session_state['url'], width=630, height=420, scrolling=True)
    st.caption(
        'If you cannot see the image, it is because the URL is incorrect or we do not have permission to access its contents.')
