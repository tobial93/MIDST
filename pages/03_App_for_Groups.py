import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from streamlit_searchbox import st_searchbox
from raffa_functions.autocomplete import *
import midst.interface.main as mdt
import pydeck as pdk
from midst.params import *
from pydeck.types import String

spell = st.secrets['spell'] # for STREAMLIT DEPLOYMENT
api_key = st.secrets.some_magic_api.API_KEY # for STREAMLIT DEPLOYMENT


# st.title('Meet me halfway! :man-kiss-man:')


st.image(['midst/images/name.png', 'midst/images/logo_alone_small.png'], use_column_width=200)


# ------
st.markdown('#### What do you and your friends want to do together?')
type_option = st.selectbox(
        'Select one thing to do at the mid point',
        (('',
            'art_gallery',
            'bakery',
            'bar',
            'beauty_salon',
            'book_store',
            'cafe',
            'clothing_store',
            'convenience_store',
            'department_store',
            'florist',
            'furniture_store',
            'gym',
            'hair_care',
            'library',
            'museum',
            'park',
            'restaurant',
            'shoe_store',
            'shopping_mall',
            'spa',
            'tourist_attraction',
            'walking')))


# -----
st.markdown('#### Select how far from the midpoint you want to receive reccomendation (in meters)')
radius = st.slider('Radius', min_value=300, max_value=700)

# ------

st.markdown('#### Provide the address and the travel mode for each person')

st.markdown('## Person 1:')
selected_location_A = st_searchbox(
search_location_A, # test in the streamlit frontend>> 'Nordhauser Straße' >> select: address_1 = 'Nordhauser Straße 2, 10589 Berlin, Deutschland'
key="location_searchbox_A",
)
option_1 = st.selectbox(
    'Person 1 Travel Mode',
    ('','transit', 'driving', 'walking', 'bicycling'))

st.markdown('## Person 2:')
selected_location_B = st_searchbox(
    search_location_B, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
    key="location_searchbox_B",
)
option_2 = st.selectbox(
    'Person 2 Travel Mode',
    ('','transit', 'driving', 'walking', 'bicycling'))

st.markdown('## Person 3:')
selected_location_C = st_searchbox(
    search_location_C, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
    key="location_searchbox_C",
)
option_3 = st.selectbox(
    'Person 3 Travel Mode',
    ('','transit', 'driving', 'walking', 'bicycling'))


st.markdown('## Person 4:')
selected_location_D = st_searchbox(
    search_location_D, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
    key="location_searchbox_D",
)
option_4 = st.selectbox(
    'Person 4 Travel Mode',
    ('','transit', 'driving', 'walking', 'bicycling'))