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
from recursion_new import *

spell = st.secrets['spell'] # for STREAMLIT DEPLOYMENT
api_key = st.secrets.some_magic_api.API_KEY # for STREAMLIT DEPLOYMENT

radius = 300

st.title('Meet me halfway! :man-kiss-man:')

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

    # From this point, the code will be in a new page

    true_midpoint = find_true_midpoint(loc_A_cords, loc_B_cords, mid_point, option_1, option_2, api_key=api_key)

    df_midpoint = pd.DataFrame([mid_point], columns = ['lat', 'lon'])
    df_true_midpoint = pd.DataFrame([true_midpoint], columns = ['lat', 'lon'])

    #---------------------------------------------
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
        <a href={url_A}><button style="background-color:Pink;">How can I get there</button></a>
        ''',
        unsafe_allow_html=True)

    with col2:
        url_B = mdt.maps_url_tomidpoint(loc_B_cords, true_midpoint)
        st.markdown(f'''
        <a href={url_B}><button style="background-color:Pink;">How can Your friend get there</button></a>
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
            get_color='[0, 100, 0, 30]',
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
            get_radius=50,
         )
    ],
))




# # find the midpoint that takes same time to arrive
#     midpoint_lat_lng = mid_point
#     # search for nearby restaurants between the two locations
#     nearby_restaurants = gmaps.places_nearby(location=midpoint_lat_lng, radius=radius, type='restaurant')

#     restaurants_name = []
#     rating = []
#     price_level = []
#     time_for_location1 = []
#     time_for_location2 =[]
#     for restaurant in nearby_restaurants['results']:
#         # get the latitude and longitude of the restaurant
#         restaurant_lat_lng = restaurant['geometry']['location']

#         # calculate the time to get to the restaurant from each location
#         directions_location1 = gmaps.directions(loc_A_cords, restaurant_lat_lng, mode="driving", departure_time=datetime.now())
#         directions_location2 = gmaps.directions(loc_B_cords, restaurant_lat_lng, mode="driving", departure_time=datetime.now())

#         restaurants_name.append(restaurant['name'])
#         time_for_location1.append(directions_location1[0]['legs'][0]['duration']['text'])
#         time_for_location2.append(directions_location2[0]['legs'][0]['duration']['text'])

#     df = pd.DataFrame({
#         'restaurants_name': restaurants_name,
#         'rating': rating,
#         'price_level': price_level,
#         'travel_time1': time_for_location1
#         'travel_time2': time_for_location2
#         })

#     #Categorize the ratings
#     rating_ranges = [(0, 2.9), (3.0, 3.9), (4.0, 4.4), (4.5, 4.9), (5.0, 5.0)]
#     rating_categories = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
#     df['rating_category'] = pd.cut(df['rating'], bins=[r[0] for r in rating_ranges] + [rating_ranges[-1][1]+0.1],
#                                  labels=rating_categories)
#     #Categorize the price level
#     def categorize_price_level(price_level):
#         if price_level == 0:
#             return "Price level not specified"
#         elif price_level == 1:
#             return "Budget-friendly"
#         elif price_level == 2:
#             return "Moderately-priced"
#         elif price_level == 3:
#             return "Expensive"
#         elif price_level == 4:
#             return "Very expensive"
#     df['price_level'] = df['price_level'].apply(lambda x: categorize_price_level(x))

#     # Get user inputs for hue variables
#     hue_cols = st.multiselect("Select columns for hue:", list(df[['rating_category','price_level']]))
#     st.write(f'you have choose {hue_cols} as your hue')
#     # Create plot
#     if hue_cols:
#         st.set_option('deprecation.showPyplotGlobalUse', False)
#         fig, ax = plt.subplots()
#         sns.scatterplot(data=df, x="travel_time1", y="travel_time1",hue=hue_cols[0],ax=ax)
#         # loop over each point and add text annotation
#         for line in range(0,df.shape[0]):
#             ax.text(df.travel_time1[line]+0.2, df.travel_time1[line], df.restaurants_name[line],
#                 horizontalalignment='left', size='medium', color='black')

#         # show the plot
#         st.pyplot(fig)
