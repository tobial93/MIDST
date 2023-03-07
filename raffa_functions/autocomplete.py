import requests
import os

API_KEY = os.environ.get("API_KEY")

api_key = API_KEY
base_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'

def location_input(string):
    params = {
        'input': string, # test with "Nordhauser Straße"
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    predictions = response.json()['predictions']
    return [prediction['description'] for prediction in predictions]

# testing def locaiton_input fuction
print(location_input("richard sorge"))