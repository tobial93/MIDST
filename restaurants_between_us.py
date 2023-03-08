import pandas as pd
import requests
import googlemaps
from datetime import datetime
import streamlit as st




# Set up Google Maps API client with your API key
midst_api_key = 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q'
gmaps = googlemaps.Client(key=midst_api_key)

# Set the API key for Google Maps and Places APIs
api_key = midst_api_key

# Define the two addresses
address1 = 'Alex-Wedding-Straße 3, 10178 Berlin'
address2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'

# Use the Google Maps API to get the latitude and longitude for each address
url = "https://maps.googleapis.com/maps/api/geocode/json"
params = {
    "address": address1,
    "key": api_key
}
response = requests.get(url, params=params).json()
location1 = response["results"][0]["geometry"]["location"]

params["address"] = address2
response = requests.get(url, params=params).json()
location2 = response["results"][0]["geometry"]["location"]

# Use the Google Places API to search for restaurants between the two locations
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": f"{location1['lat']},{location1['lng']}",
    "radius": 5000,
    "type": "restaurant",
    "key": api_key
}
response = requests.get(url, params=params).json()
results1 = response["results"]

params["location"] = f"{location2['lat']},{location2['lng']}"
response = requests.get(url, params=params).json()
results2 = response["results"]

# Combine the results from the two searches into one list
results = results1 + results2

# Create a pandas dataframe from the results
df = pd.DataFrame(results)
df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])
# Print the dataframe

df.to_csv('my_dataframe1.csv', index=False)
