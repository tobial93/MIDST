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
key = st.secrets.some_magic_api.API_KEY_STREAMLIT_SECRET # for STREAMLIT DEPLOYMENT


radius = 300

st.title('Meet me halfway! :man-kiss-man:')

col1, col2 = st.columns(2)

with col1:
    st.markdown('## I am at :round_pushpin:')
    selected_location_A = st_searchbox(
    search_location_A, # test in the streamlit frontend>> 'Nordhauser Straße' >> select: address_1 = 'Nordhauser Straße 2, 10589 Berlin, Deutschland'
    key="location_searchbox_A",
)
    option = st.selectbox(
        'How do you want to get there?',
        ('Public transportation', 'Car', 'walking'))

    st.write('You selected:', option)
with col2:
    st.markdown('## My friend is at :round_pushpin:')
    selected_location_B = st_searchbox(
        search_location_B, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
        key="location_searchbox_B",
    )
    # df2 = pd.DataFrame([[52.5318236,13.3481977]], columns=['lat', 'lon'])
    # st.map(df2)
    option2 = st.selectbox(
        'How does your friend want to get there?',
        ('Public transportation', 'Car', 'walking'))
    st.write('You selected for your friend:', option)

type_option = st.selectbox(
        'Things to do at the mid point',
        (('Select activity',
            'amusement_park',
            'aquarium',
            'art_gallery',
            'bakery',
            'bar',
            'beauty_salon',
            'book_store',
            'bowling_alley',
            'cafe',
            'campground',
            'casino',
            'clothing_store',
            'convenience_store',
            'department_store',
            'florist',
            'furniture_store',
            'gas_station',
            'gym',
            'hair_care',
            'home_goods_store',
            'jewelry_store',
            'laundry',
            'library',
            'mosque',
            'movie_theater',
            'museum',
            'night_club',
            'park',
            'pet_store',
            'physiotherapist',
            'restaurant',
            'shoe_store',
            'shopping_mall',
            'spa',
            'store',
            'supermarket',
            'tourist_attraction',
            'zoo')))

if selected_location_A and selected_location_B:
    loc_A_cords = mdt.get_lat_lon(selected_location_A, key) # for STREAMLIT DEPLOYMENT we are passing API_KEY called key
    loc_B_cords = mdt.get_lat_lon(selected_location_B, key) # for STREAMLIT DEPLOYMENT we are passing API_KEY called key
    mid_point = mdt.midpoint(loc_A_cords,loc_B_cords)
    places_json = mdt.places(mid_point, radius=radius, type=str(type_option)).json()
    places_list = mdt.coords_name(places_json)
    df = pd.DataFrame(places_list, columns=['lat', 'lon', 'name'])
    df_midpoint = pd.DataFrame([mid_point], columns = ['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(map_style=pdk.map_styles.ROAD, initial_view_state=pdk.ViewState(
        latitude=mid_point[0],
        longitude=mid_point[1],
        zoom=15
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_midpoint,
            get_position='[lon, lat]',
            get_color='[0, 0, 100, 30]',
            get_radius=radius,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=10,
        ),
        pdk.Layer(
            "TextLayer",
            data = df,
            sizeScale = 0.4,
            pickable=True,
            get_position='[lon, lat]',
            get_text='name',
            get_size=16,
            get_color=[0, 0, 0],
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("bottom"),
        )
    ],
))
