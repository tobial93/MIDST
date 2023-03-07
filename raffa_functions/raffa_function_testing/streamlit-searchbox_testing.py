from typing import List
import wikipedia

import streamlit as st
from streamlit_searchbox import st_searchbox


# -----------TESTING LIST----------
# """Example1 function that takes a list of integers and returns a new list"""
def process_list_int_by2(my_list: List[int]) -> List[int]:
    """Example function that takes a list of integers and returns a new list"""
    new_list = [x * 2 for x in my_list]
    return new_list

# TESTING Example1

my_list_int = [1, 2, 3, 4, 5]
new_list1 = process_list_int_by2(my_list_int)
print(new_list1)


# """Example2 function that takes a list of strings and returns a new list"""
def process_list_string_to_upper(my_list: List[str]) -> List[str]:
    """Example function that takes a list of strings and returns a new list"""
    new_list = [s.upper() for s in my_list]
    return new_list

# TESTING Example2
my_list_string = ["apple", "banana", "orange"]
new_list_2 = process_list_string_to_upper(my_list_string)
print(new_list_2)

#---------TESTING WIKIPEDIA & SEARCHBOX----------
# function with list of labels
def search_wikipedia(searchterm) -> List[str]:
    return wikipedia.search(searchterm) if searchterm else []

#TESTING search term
search_results = search_wikipedia("coding bootcamp")
print(search_results)
#OUTPUT: ['Coding bootcamp', 'Dev Bootcamp', 'Boot camp', 'Fullstack Academy', 'Bloom Institute of Technology', 'Hack Reactor', 'App Academy', 'Coding House', 'Flatiron School', 'Trilogy Education Services']

# pass search function to searchbox
# selected_value = st_searchbox(
#     search_wikipedia,
#     key="wiki_searchbox",
# )
# st.markdown("You've selected: %s" % selected_value)


#------------TETING PLACES AUTOCOMPLETE API---------

import requests

israel_api_key = 'AIzaSyAa7smWhdougw5OHY5ek13d4cf6AsZH4rM'
midst_api_key = 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q'

# api_key = midst_api_key
# base_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'

# params = {
#     'input': 'starbucks near me',
#     'key': api_key
# }

# response = requests.get(base_url, params=params)
# predictions = response.json()['predictions']

# for prediction in predictions:
#     print(prediction['description'])


#------------TETING PLACES AUTOCOMPLETE API w/Full Params---------

api_key = midst_api_key

base_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'

params = {
    'input': 'Nordhauser Straße', # Full Address: Nordhauser Straße 2, 10589 Berlin, Deutschland
    'location': '52.5200,13.4050',
    #'radius': '1000',
    #'components': 'administrative_area:Berlin',
    #'types': 'establishment',
    #'language': 'de',
    #'strictbounds': 'true',
    'key': api_key
}

response = requests.get(base_url, params=params)
predictions = response.json()['predictions']

for prediction in predictions:
    print(prediction['description'])


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