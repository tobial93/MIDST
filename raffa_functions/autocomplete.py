import requests
import os
from typing import List#, Dict

API_KEY = os.environ.get("API_KEY")


# AUTOCOMPLETE Component using autocomplete API
api_key = API_KEY
base_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'


def location_input(string):
    params = {
        'input': string,
        'key': api_key
    }
        
    response = requests.get(base_url, params=params)
    predictions = response.json()['predictions']
    return [prediction['description'] for prediction in predictions]

# def location_input_B(string): 
#     params = {
#         'input': string,
#         'key': api_key
#     }
    
#     response = requests.get(base_url, params=params)
#     predictions = response.json()['predictions']
#     return [prediction['description'] for prediction in predictions]

# SEARCHBOX Component: Pass location_input to searchbox feature in streamlit list format
def search_location_A(searchterm, rerun=False) -> List[str]:
    return location_input(searchterm) if searchterm else []

def search_location_B(searchterm, rerun=False) -> List[str]:
    return location_input(searchterm) if searchterm else []



# SEARCHBOX Component_v2: Pass location_input to searchbox feature in streamlit list format

# def search_location_both(searchterm) -> Dict[str, List[str]]:
#     if not searchterm:
#         return {"location_A": [], "location_B": []}

#     location_A_predictions = location_input(searchterm + " A")
#     location_B_predictions = location_input(searchterm + " B")

#     return {"location_A": location_A_predictions, "location_B": location_B_predictions}



# ---------TESTING IN GIT-----------------
# testing def locaiton_input fuction while running autocomplete.py file in git
print(location_input("le wagon 26"))
print(location_input("richard sorge"))

