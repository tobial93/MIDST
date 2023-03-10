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
import pydeck as pdk
from midst.params import *
from pydeck.types import String


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
    number_of_results = len(places_json['results'])
    st.write(f'we found {number_of_results} places for you')
    for place in places_json['results']:
        # get the latitude and longitude of the restaurant
        place_lat_lng = place['geometry']['location']

        # calculate the time to get to the restaurant from each location
        directions_location1 = gmaps.directions(loc_A_cords, place_lat_lng, mode="driving", departure_time=datetime.now())
        directions_location2 = gmaps.directions(loc_B_cords, place_lat_lng, mode="transit", departure_time=datetime.now())

        results_name.append(place['name'])
        st.write(place['name'])
        #we take the minutes as int to arrive
        mins_for_location1 = int(directions_location1[0]['legs'][0]['duration']['text'][0])
        time_for_location1.append(mins_for_location1)
        mins_for_location2 = int(directions_location2[0]['legs'][0]['duration']['text'][0])
        time_for_location2.append(mins_for_location2)
        try:
            price_level.append(place['price_level'])
        except:
            price_level.append(0)
        try:
            rating.append(place['rating'])
        except:
            rating.append(0)


    df_results = pd.DataFrame({
        'results_name': results_name,
        'rating': rating,
        'price_level': price_level,
        'travel_time1': time_for_location1,
        'travel_time2': time_for_location2 })

    #Categorize the ratings
    rating_ranges = [(0, 2.9), (3.0, 3.9), (4.0, 4.4), (4.5, 4.9), (5.0, 5.0)]
    rating_categories = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
    df_results['rating_category'] = pd.cut(df_results['rating'], bins=[r[0] for r in rating_ranges] + [rating_ranges[-1][1]+0.1],
                                 labels=rating_categories)

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
    hue_cols = st.multiselect("Select columns for hue:", list(df_results[['rating_category','price_level']]))
    st.write(f'you have choose {hue_cols} as your hue')
    # Create plot
    if hue_cols:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df_results, x="travel_time1", y="travel_time1",hue=hue_cols[0],ax=ax)
        # loop over each point and add text annotation
        for line in range(0,df_results.shape[0]):
            ax.text(df_results.travel_time1[line]+0.2,  df_results.travel_time1[line],  df_results.results_name[line],
                horizontalalignment='left', size='medium', color='black')

        # show the plot
        st.pyplot(fig)
