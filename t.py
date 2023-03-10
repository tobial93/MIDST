import googlemaps
from datetime import datetime
import streamlit as st
import pandas as pd
import os
import seaborn as sns
import plotly.express as px
import requests
import matplotlib.pyplot as plt

API_KEY = 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q'
gmaps = googlemaps.Client(key=API_KEY)
def places(lat_long:tuple, radius:int, type:str):
    '''
    Returns a JSON dict with a list of places arround a point
    specified by latitude and longitude imputed as a tuple
    in a certan radius from this point
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    location = f'{lat_long[0]},{lat_long[1]}'
    params = {
        'location' : location,
        'radius' : str(radius),
        'type' : str(type),
        'key' : API_KEY
    }
    # url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={API_KEY}"

    places_json = requests.get(url=base_url, params=params)

    # for places in range(len(places_json['results']))
    return places_json
mid_point = [52.5211188,13.3898133]
places_json = places(mid_point, radius=300, type='restaurant').json()
places = places_json['results']
print(places[0]['price_level'])



#df = pd.DataFrame(places)
ti = int(gmaps.directions([52.5211188,13.3898133], [52.5517471,13.4384512], mode="transit", departure_time=datetime.now())[0]['legs'][0]['duration']['text'][0])
print(type(ti))
print(ti-4)
print(ti)
#ti2 = gmaps.directions([52.5211188,13.3898133], [52.5517471,13.4384512], mode="driving", departure_time=datetime.now())[0]['legs'][0]['duration']['text']
#print(ti2)

#df.to_csv('myetest.csv', index=False)
