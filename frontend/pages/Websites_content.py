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


# get website content from api endpoint
def get_website_content(website_url):
    # call the api
    payload = json.dumps([{"url": website_url}])
    headers = {"Content-Type": "application/json"}
    url = os.environ["API_ENDPOINT"] + "/website/content"
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()
    return results


# function to display all the website content
def render_website_content(website_url):
    with st.expander("Website URL", expanded=True):
        st.write("The website is: ", website_url)

    tab1, tab2, tab3, tab4 = st.tabs(["Title", "Class", "Summary", "Preview"])
    title, summary = get_website_content(website_url)

    with tab1:
        st.write(f'The website title is: {title}.')
    with tab2:
        st.write(f"The website was classified as {st.session_state['results']}.")
    with tab3:
        st.write(f"Summary: {summary}")
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


# page configuration
st.set_page_config(page_title='LinkScribe', page_icon=':globe_with_meridians:', layout='wide')
st.header('LinkScribe')
st.subheader('Website Content 💻')

st.write("Here, you can find the summary of the content of the website you classified above.")

website_url = st.session_state['url']

# verifies whether the URL was provided or not
if website_url:
    render_website_content(website_url)
else:
    st.image('web.jpg', use_column_width=True)
    st.error(":blue[Website URL not provided.]", icon="🚨")
