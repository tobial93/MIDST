import streamlit as st
import pandas as pd
import datetime
import requests
import numpy as np
import pydeck as pdk
st.title('Meet me halfway! :man-kiss-man:')


col1, col2 = st.columns(2)

with col1:
    st.markdown('## I am at :round_pushpin:')
    st.write('##### Here will be a drop down menu for user to put an address:')
    option = st.selectbox(
        'How do you want to get there?',
        ('Public transportation', 'Car', 'walking'))

    st.write('You selected:', option)
with col2:
    st.markdown('## My friend is at :round_pushpin:')
    st.write('##### Here will be another drop down menu for user to put another address:')
    df2 = pd.DataFrame([[52.5318236,13.3481977]], columns=['lat', 'lon'])
    st.map(df2)
    option2 = st.selectbox(
        'How does your friend want to get there?',
        ('Public transportation', 'Car', 'walking'))
    st.write('You selected for your friend:', option)

df = pd.DataFrame([[52.5318236,13.3481977],[52.5544694,13.4280902]], columns=['lat', 'lon'])
st.map(df)
