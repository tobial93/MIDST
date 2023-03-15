import streamlit as st
import pandas as pd
import googlemaps
import datetime
import pydeck as pdk
from pydeck.types import String
import plotly.express as px
import urllib.parse


st.sidebar.title('Your MIDST recommendations')
st.title("These are Your MIDST recommendations")

spell = st.secrets['spell'] # for STREAMLIT DEPLOYMENT
api_key = st.secrets.some_magic_api.API_KEY # for STREAMLIT DEPLOYMENT
gmaps = googlemaps.Client(key=api_key)

if st.session_state.type_option != '':
    results_name = []
    rating = []
    price_level = []
    price_level_ = []
    time_for_location1 = []
    time_for_location2 = []
    time_for_location1_ = []
    time_for_location2_ = []
    result_address= []
    number_of_results = len(st.session_state.places_json['results'])
    st.write(f'#### We have found {number_of_results} places for You and Your friend!')

    for place in st.session_state.places_json['results']:
        # get the latitude and longitude of the restaurant
        place_lat_lng = place['geometry']['location']

        # calculate the time to get to the restaurant from each location
        directions_location1 = gmaps.directions(st.session_state.loc_A_cords, place_lat_lng, mode=st.session_state.option_1, departure_time=datetime.datetime.now())
        directions_location2 = gmaps.directions(st.session_state.loc_B_cords, place_lat_lng, mode=st.session_state.option_2, departure_time=datetime.datetime.now())
        result_address.append(place['vicinity'])
        results_name.append(place['name'])
        #we take the minutes as int to arrive

        # for_location1 = int(directions_location1[0]['legs'][0]['duration']['value'])
        # time_for_location1.append(for_location1)

        for_location1 = int(directions_location1[0]['legs'][0]['duration']['value'])
        in_seconds1 = datetime.timedelta(seconds=for_location1)
        minutes1, seconds1 = divmod(in_seconds1.seconds, 60)
        minutes_1 = in_seconds1.seconds/60
        time_for_location1.append(f"{minutes1} min {seconds1} sec")
        time_for_location1_.append(round(minutes_1, 2))

        # for_location2 = int(directions_location2[0]['legs'][0]['duration']['value'])
        # time_for_location2.append(for_location2)

        for_location2 = int(directions_location2[0]['legs'][0]['duration']['value'])
        in_seconds2 = datetime.timedelta(seconds=for_location2)
        minutes2, seconds2 = divmod(in_seconds2.seconds, 60)
        minutes_2 = in_seconds2.seconds/60
        time_for_location2.append(f"{minutes2} min {seconds2} sec")
        time_for_location2_.append(round(minutes_2, 2))




        # get the price level
        try:
            price_level.append(place['price_level'])
        except:
            price_level.append(0)

        try:
            if place['price_level'] == 0:
                price_level_.append("Not specified")
            if place['price_level'] == 1:
                price_level_.append("Budget-friendly")
            if place['price_level'] == 2:
                price_level_.append("Moderately-priced")
            if place['price_level'] == 3:
                price_level_.append("Expensive")
            if place['price_level'] == 4:
                price_level_.append("Very expensive")
        except:
            price_level_.append("Not specified")


        # categorize rate_level
        try:
            if place['rating'] > 4.5                                             :
                rating.append('1-Excellent')
            elif place['rating'] > 4:
                rating.append('2-Good')
            elif place['rating'] > 3:
                rating.append('3-Average')
            elif place['rating'] > 2:
                rating.append('4-Poor')
            else:
                rating.append('5-Terrible')
        except:
            rating.append('6-Unrated')


    df_results = pd.DataFrame({
        'Name': results_name,
        'Rating': rating,
        'Pricing': price_level_,
        'Time for YOU': time_for_location1,
        'Time for YOUR friend': time_for_location2,
        'Address': result_address})

    st.markdown('Click on the column names to sort your results')
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
    df_results['Pricing'] =  df_results['Pricing'].apply(lambda x: categorize_price_level(x))

#----------------------------------------------------------------------------------------------------------------
    # # Get user inputs for hue variables
    # hue_cols = st.multiselect("How long does it take to gete there? Compare your times on the next image, select your criteria:", ['rating','price_level'])
    # st.write('You can hover on the plot to see whats the option that fits you better')

    # # Create plot
    # if hue_cols:
    #     st.set_option('deprecation.showPyplotGlobalUse', False)
    #     #assign the second hue
    #     def get_second_item(my_list):
    #         if len(my_list) == 2:
    #             return my_list[1]
    #         else:
    #             return None
    #     fig = px.scatter(df_results, x='Time for YOU', y='Time for YOUR friend', hover_data=['result_name'],color=hue_cols[0], symbol=get_second_item(hue_cols))
    #     # Add column as annotation
    #     #fig.add_trace(go.Scatter(x=df_results['travel_time1'], y=df_results['travel_time2'],
    #            #text=df_results['result_name'], mode='text'))

    #     # Display Plotly figure in Streamlit app
    #     st.plotly_chart(fig)
# -------------------------------------------------------------------------------------------------------------
    options = df_results['Name']
    st.write('#### Select your prefered location:')
    chosen_place = st.selectbox(label = '', options = options)
    #Find the address the chosen place
    df_results.set_index('Name', inplace=True)
    destination = df_results.loc[chosen_place, 'Address']

    col3, col4 = st.columns(2)

    with col3:
        url_person_A = f"https://www.google.com/maps/dir/{urllib.parse.quote(st.session_state.selected_location_A)}/{urllib.parse.quote(destination)}"
        st.markdown(f'''
        <a href={url_person_A}><button style="background-color:#ffde5a;">How You can get there</button></a>
        ''',
        unsafe_allow_html=True)
    with col4:
        url_person_B = f"https://www.google.com/maps/dir/{urllib.parse.quote(st.session_state.selected_location_B)}/{urllib.parse.quote(destination)}"
        st.markdown(f'''
        <a href={url_person_B}><button style="background-color:#ffde5a;">How can Your friend get there</button></a>
        ''',
        unsafe_allow_html=True)
#---------------------------------------------------------------------------------------------------------------
#new

    df_results_2 = pd.DataFrame({
        'Name': results_name,
        'Rating': rating,
        'Pricing': price_level,
        'Time for YOU (Min)': time_for_location1_,
        'Time for YOUR friend (Min)': time_for_location2_,
        'Location': result_address})

    # Get user inputs for hue variables
    st.write('### ')
    st.write('### How long does it take to get there?')

    hue_cols = st.multiselect("Compare your times with our visual tool, just select an option:", ['Rating','Pricing'])

    if hue_cols:
        st.write('### ')
        st.write('You can hover on the plot to see what option fits you better')

    # Create plot
        st.set_option('deprecation.showPyplotGlobalUse', False)
        #assign the second hue
        def get_second_item(my_list):
            if len(my_list) == 2:
                return my_list[1]
            else:
                return None
        fig = px.scatter(df_results_2, x='Time for YOU (Min)', y='Time for YOUR friend (Min)', hover_data=['Name'],color=hue_cols[0], symbol=get_second_item(hue_cols))
        # Add column as annotation
        #fig.add_trace(go.Scatter(x=df_results['travel_time1'], y=df_results['travel_time2'],
               #text=df_results['result_name'], mode='text'))

        # Display Plotly figure in Streamlit app
        st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------

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

else:
    st.error("Please complete the fields in the Main site")
