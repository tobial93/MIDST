import streamlit as st
import pandas as pd
import googlemaps
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
from streamlit_searchbox import st_searchbox
from raffa_functions.autocomplete import *
import midst.interface.main as mdt
from midst.params import *
from pydeck.types import String
import plotly.express as px
import plotly.graph_objs as go
import webbrowser
import urllib.parse


st.set_page_config(page_title='Contacts')

st.write("This is the reccomendations page\n")



spell = st.secrets['spell'] # for STREAMLIT DEPLOYMENT
api_key = st.secrets.some_magic_api.API_KEY # for STREAMLIT DEPLOYMENT
gmaps = googlemaps.Client(key=api_key)
radius = 300

st.title('Meet me halfway! :man-kiss-man:')

col1, col2 = st.columns(2)

with col1:
    st.markdown('## I am at :round_pushpin:')
    selected_location_A = st_searchbox(
    search_location_A, # test in the streamlit frontend>> 'Nordhauser Straße' >> select: address_1 = 'Nordhauser Straße 2, 10589 Berlin, Deutschland'
    key="location_searchbox_A",
)
    # option = st.selectbox(
    #     'How do you want to get there?',
    #     ('Public transportation', 'Car', 'walking'))

    # st.write('You selected:', option)
with col2:
    st.markdown('## My friend is at :round_pushpin:')
    selected_location_B = st_searchbox(
        search_location_B, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
        key="location_searchbox_B",
    )
    # df2 = pd.DataFrame([[52.5318236,13.3481977]], columns=['lat', 'lon'])
    # st.map(df2)
    # option2 = st.selectbox(
    #     'How does your friend want to get there?',
    #     ('Public transportation', 'Car', 'walking'))
    # st.write('You selected for your friend:', option)

type_option = st.selectbox(
        'Things to do at the mid point',
        (('',
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

if selected_location_B and type_option:
    loc_A_cords = mdt.get_lat_lon(selected_location_A, api_key) # for STREAMLIT DEPLOYMENT we are passing API_KEY called key
    loc_B_cords = mdt.get_lat_lon(selected_location_B, api_key) # for STREAMLIT DEPLOYMENT we are passing API_KEY called key
    mid_point = mdt.midpoint(loc_A_cords,loc_B_cords)
    places_json = mdt.places(mid_point, radius=radius, type=str(type_option), API_KEY=api_key).json()
    places_list = mdt.coords_name(places_json)
    df = pd.DataFrame(places_list, columns=['lat', 'lon', 'name'])
    df_midpoint = pd.DataFrame([mid_point], columns = ['lat', 'lon'])

    with col1:
        url_A = mdt.maps_url_tomidpoint(loc_A_cords, mid_point)
        st.markdown(f'''
        <a href={url_A}><button style="background-color:Pink;">How can I get there</button></a>
        ''',
        unsafe_allow_html=True)

    with col2:
        url_B = mdt.maps_url_tomidpoint(loc_B_cords, mid_point)
        st.markdown(f'''
        <a href={url_B}><button style="background-color:Pink;">How can Your friend get there</button></a>
        ''',
        unsafe_allow_html=True)

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

    results_name = []
    rating = []
    price_level = []
    time_for_location1 = []
    time_for_location2 =[]
    result_address= []
    number_of_results = len(places_json['results'])
    st.write(f'we found {number_of_results} places for you')

    for place in places_json['results']:
        # get the latitude and longitude of the restaurant
        place_lat_lng = place['geometry']['location']

        # calculate the time to get to the restaurant from each location
        directions_location1 = gmaps.directions(loc_A_cords, place_lat_lng, mode="driving", departure_time=datetime.now())
        directions_location2 = gmaps.directions(loc_B_cords, place_lat_lng, mode="transit", departure_time=datetime.now())
        result_address.append(place['vicinity'])
        results_name.append(place['name'])
        #we take the minutes as int to arrive
        for_location1 = int(directions_location1[0]['legs'][0]['duration']['value'])
        time_for_location1.append(for_location1)
        for_location2 = int(directions_location2[0]['legs'][0]['duration']['value'])
        time_for_location2.append(for_location2)
        # get the price level
        try:
            price_level.append(place['price_level'])
        except:
            price_level.append(0)
        # categorize rate_level
        try:
            if place['rating'] > 4.5                                             :
                rating.append('Excellent')
            elif place['rating'] > 4:
                rating.append('Good')
            elif place['rating'] > 3:
                rating.append('Average')
            elif place['rating'] > 2:
                rating.append('Poor')
            else:
                rating.append('Terriable')
        except:
            rating.append('NA')


    df_results = pd.DataFrame({
        'result_name': results_name,
        'rating': rating,
        'price_level': price_level,
        'time_personA': time_for_location1,
        'time_personB': time_for_location2,
        'location': result_address})

    st.markdown('#### All the suggestions are here, please click on the column name for different rankings')
    st.write(df_results)
    #Categorize the price level
    def categorize_price_level(price_level):
        if price_level == 0:
            return "Price level not specified"
        elif price_level == 1:
            return "Budget-friendly"
        elif price_level == 2:
            return "Moderately-priced"
        elif price_level == 3:
            return "Expensive"
        elif price_level == 4:
            return "Very expensive"
    df_results['price_level'] =  df_results['price_level'].apply(lambda x: categorize_price_level(x))

    # Get user inputs for hue variables
    hue_cols = st.multiselect("Please select your criteria:", ['rating','price_level'])
    st.write(f'you have choose {hue_cols} as your criteria. Please hover around the plot to see the details of each recommendation and find your best option')

    # Create plot
    if hue_cols:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        #assign the second hue
        def get_second_item(my_list):
            if len(my_list) == 2:
                return my_list[1]
            else:
                return None
        fig = px.scatter(df_results, x='time_personA', y='time_personB', hover_data=['result_name'],color=hue_cols[0], symbol=get_second_item(hue_cols))
        # Add column as annotation
        #fig.add_trace(go.Scatter(x=df_results['travel_time1'], y=df_results['travel_time2'],
               #text=df_results['result_name'], mode='text'))

        # Display Plotly figure in Streamlit app
        st.plotly_chart(fig)

        options = df_results['result_name']
        chosen_place = st.selectbox('Please select one place here', options)
        st.write('You selected:', chosen_place)
        st.write('Please click on the buttons below to see how to get there')
        #Find the address the chosen place
        df_results.set_index('result_name', inplace=True)
        destination = df_results.loc[chosen_place, 'location']

        col3, col4 = st.columns(2)

        with col3:
            url_person_A = f"https://www.google.com/maps/dir/{urllib.parse.quote(selected_location_A)}/{urllib.parse.quote(destination)}"
            #st.write(url_person_A)
            if st.button("How person A can get to this place"):
                webbrowser.open_new_tab(url_person_A)
        with col4:
            url_person_B = f"https://www.google.com/maps/dir/{urllib.parse.quote(selected_location_B)}/{urllib.parse.quote(destination)}"
            if st.button("How person B can get to this place"):
                webbrowser.open_new_tab(url_person_B)