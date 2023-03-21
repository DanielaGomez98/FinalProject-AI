import os
import time
import streamlit as st
from decouple import config
from app.services import UrlLabelService

# set the api endpoint
if "API_ENDPOINT" not in os.environ:
    os.environ["API_ENDPOINT"] = config("API_ENDPOINT")

labels_service = UrlLabelService()

st.set_page_config(page_title='LinkScribe',
                   page_icon=':globe_with_meridians:',
                   layout='wide')
st.sidebar.title('Options')

st.header('LinkScribe')
st.subheader('Website Classification 🔍')
st.image('web3.jpg', use_column_width=True)

st.write('LinkScribe is a web application that uses Machine Learning to allow you to create and organize lists of links easily and efficiently. '
         'With LinkScribe, you can simply copy and paste a web link, and the application will automatically process it, extracting information '
         'about the page content and classifying them according to the information obtained.')

st.write(':blue[Enter a website URL to classify its content:]')
url = st.text_input('URL', '')


classify = st.button('Classify')

if classify:
    with st.spinner('Wait for it...'):
        time.sleep(2)
    results = labels_service.add_url(url)
    st.success(f'Done!✅ This website URL {url} is classified as {results["label"][0]}.')
    st.balloons()
    st.caption('You can see a summary of the website content on the "Websites Content" page.')

    if results not in st.session_state:
        st.session_state["results"] = results["label"][0]

if url not in st.session_state:
    st.session_state["url"] = url
