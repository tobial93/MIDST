import streamlit as st
import pandas as pd
import googlemaps
from datetime import datetime
import pydeck as pdk
from pydeck.types import String
import plotly.express as px
import webbrowser
import urllib.parse

st.title("These are Your recomendations")

spell = st.secrets['spell'] # for STREAMLIT DEPLOYMENT
api_key = st.secrets.some_magic_api.API_KEY # for STREAMLIT DEPLOYMENT
gmaps = googlemaps.Client(key=api_key)

results_name = []
rating = []
price_level = []
time_for_location1 = []
time_for_location2 =[]
result_address= []
number_of_results = len(st.session_state.places_json['results'])
st.write(f'We found {number_of_results} places for you')

for place in st.session_state.places_json['results']:
    # get the latitude and longitude of the restaurant
    place_lat_lng = place['geometry']['location']

    # calculate the time to get to the restaurant from each location
    directions_location1 = gmaps.directions(st.session_state.loc_A_cords, place_lat_lng, mode=st.session_state.option_1, departure_time=datetime.now())
    directions_location2 = gmaps.directions(st.session_state.loc_B_cords, place_lat_lng, mode=st.session_state.option_2, departure_time=datetime.now())
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
st.write(f'You have choose {hue_cols} as your criteria. Please hover around the plot to see the details of each recommendation and find your best option')

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
        url_person_A = f"https://www.google.com/maps/dir/{urllib.parse.quote(st.session_state.selected_location_A)}/{urllib.parse.quote(destination)}"
        #st.write(url_person_A)
        if st.button("How You can get to this place"):
            webbrowser.open_new_tab(url_person_A)
    with col4:
        url_person_B = f"https://www.google.com/maps/dir/{urllib.parse.quote(st.session_state.selected_location_B)}/{urllib.parse.quote(destination)}"
        if st.button("How Your friend can get to this place"):
            webbrowser.open_new_tab(url_person_B)

st.pydeck_chart(pdk.Deck(map_style=pdk.map_styles.ROAD, initial_view_state=pdk.ViewState(
                latitude=st.session_state.true_midpoint[0],
                longitude=st.session_state.true_midpoint[1],
                zoom=15
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=st.session_state.df_true_midpoint,
                    get_position='[lon, lat]',
                    get_color='[0, 0, 100, 30]',
                    get_radius=st.session_state.radius,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=st.session_state.df_midpoint,
                    get_position='[lon, lat]',
                    get_color='[100, 0, 0, 200]',
                    get_radius=15,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=st.session_state.df,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=10,
                ),
                pdk.Layer(
                    "TextLayer",
                    data = st.session_state.df,
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
                data=st.session_state.df_locations,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 200]',
                get_radius=15,
            ),
            pdk.Layer(
                "TextLayer",
                data = st.session_state.df_locations,
                sizeScale = 0.8,
                pickable=True,
                get_position='[lon, lat]',
                get_text='name',
                get_size=16,
                get_color=[255, 0, 0],
                get_angle=0,
                # Note that string constants in pydeck are explicitly passed as strings
                # This distinguishes them from columns in a data set
                get_text_anchor=String("middle"),
                get_alignment_baseline=String("bottom")
            ),
            ],
            ))
