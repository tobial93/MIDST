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

col1, col2 = st.columns(2)

with col1:
    st.markdown('## I am at :round_pushpin:')
    selected_location_A = st_searchbox(
    search_location_A, # test in the streamlit frontend>> 'Nordhauser Straße' >> select: address_1 = 'Nordhauser Straße 2, 10589 Berlin, Deutschland'
    key="location_searchbox_A",
)
    option_1 = st.selectbox(
        'How do you want to get there?',
        ('','transit', 'driving', 'walking', 'bicycling'))

with col2:
    st.markdown('## My friend is at :round_pushpin:')
    selected_location_B = st_searchbox(
        search_location_B, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
        key="location_searchbox_B",
    )
    option_2 = st.selectbox(
        'How does your friend want to get there?',
        ('','transit', 'driving', 'walking', 'bicycling'))

# type_option = st.selectbox(
#         'Things to do at the mid point',
#         ('',
#         'airport',
#         'bus_station',
#         'campground',
#         'gas_station',
#         'lodging',
#         'meal_delivery',
#         'meal_takeaway',
#         'parking',
#         'public_transportation',
#         'rv_park',
#         'subway_station',
#         'taxi_stand',
#         'train_station',
#         'transit_station'))
type_option = st.selectbox(
        'Things to do at the mid point',
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

radius = st.slider('Radius', min_value=300, max_value=700)

if selected_location_B and type_option:
    loc_A_cords = mdt.get_lat_lon(selected_location_A, api_key)
    loc_B_cords = mdt.get_lat_lon(selected_location_B, api_key)
    mid_point = mdt.midpoint(loc_A_cords,loc_B_cords)

    true_midpoint = mdt.find_true_midpoint(loc_A_cords, loc_B_cords, mid_point, option_1, option_2, API_KEY=api_key)

    df_midpoint = pd.DataFrame([mid_point], columns = ['lat', 'lon'])
    df_true_midpoint = pd.DataFrame([true_midpoint], columns = ['lat', 'lon'])

    places_json = mdt.places(true_midpoint, radius=radius, type=str(type_option), API_KEY=api_key).json()
    places_list = mdt.coords_name(places_json)
    df = pd.DataFrame(places_list, columns=['lat', 'lon', 'name'])

    sel_locs = []

    sel_locs.append(loc_A_cords)
    sel_locs.append(loc_B_cords)

    df_locations = pd.DataFrame(sel_locs, columns=['lat','lon'])

    with col1:
        url_A = mdt.maps_url_tomidpoint(loc_A_cords, true_midpoint)
        st.markdown(f'''
        <a href={url_A}><button style="background-color:#ffde5a;">How can I get there</button></a>
        ''',
        unsafe_allow_html=True)

    with col2:
        url_B = mdt.maps_url_tomidpoint(loc_B_cords, true_midpoint)
        st.markdown(f'''
        <a href={url_B}><button style="background-color:#ffde5a;">How can Your friend get there</button></a>
        ''',
        unsafe_allow_html=True)

    st.pydeck_chart(pdk.Deck(map_style=pdk.map_styles.ROAD, initial_view_state=pdk.ViewState(
        latitude=true_midpoint[0],
        longitude=true_midpoint[1],
        zoom=15
    ),
    layers=[
         pdk.Layer(
            'ScatterplotLayer',
            data=df_true_midpoint,
            get_position='[lon, lat]',
            get_color='[0, 0, 100, 30]',
            get_radius=radius,
         ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df_midpoint,
            get_position='[lon, lat]',
            get_color='[100, 0, 0, 200]',
            get_radius=15,
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
            sizeScale = 0.6,
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
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df_locations,
            get_position='[lon, lat]',
            get_color='[100, 0, 0, 200]',
            get_radius=15,
         )
    ],
))
