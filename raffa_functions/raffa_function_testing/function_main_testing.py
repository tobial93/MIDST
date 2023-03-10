import googlemaps
import requests
import json
from midst.params import *
from midst.interface.main import *

import streamlit as st
from streamlit_searchbox import st_searchbox



print("---------------------------------------")  
print("------------maps_url_tomidpoint_aa-----")  
# fucntion 1 try
def maps_url_tomidpoint_aa(location_A:tuple, midpoint_aa:tuple):
    '''
    Returns a map link.
    Needs 4 integers
    The starting point is the location A lat/lng.
    The destination point is the midpoint lat/lnhg
    '''
    start_lat = location_A[0]
    start_lng = location_A[1]
    midpoint_lat = midpoint_aa[0] 
    midpoint_lng = midpoint_aa[1]

    maps_url_tomidpoint_1 = f"https://www.google.com/maps/dir/{start_lat},{start_lng}/{midpoint_lat},{midpoint_lng}"
    return maps_url_tomidpoint_1

# Example usage function 1 try:
location_A = (52.494947, 13.479381)  # Richard-Sorge-Straße 21
midpoint_aa = (52.5104661, 13.432039)  # midpoint between location A and Le Wagon Berlin
url_1 = maps_url_tomidpoint_aa(location_A, midpoint_aa)
print(url_1)
print("check the file named: function_main_testing.py for STREAMLIT code implementation")
#streamlit code implementation
'''markdown_url_1 = f"[{url_1}]({url_1})" 
st.markdown(markdown_url_1, unsafe_allow_html=True)'''



print("---------------------------------------")  
print("------------maps_url_tomidpoint_bb-----")  
# function 2 try
def maps_url_tomidpoint_bb(location_A: tuple, midpoint_bb: tuple):
    '''
    Returns a clickable hyperlink to Google Maps.
    The starting point is the location A lat/lng.
    The destination point is the midpoint lat/lng.
    '''
    start_lat, start_lng = location_A
    midpoint_lat, midpoint_lng = midpoint_bb
    maps_url_tomidpoint_2 = f"https://www.google.com/maps/dir/{start_lat},{start_lng}/{midpoint_lat},{midpoint_lng}"
    return maps_url_tomidpoint_2


# Example usage function 2 try:
location_A = (52.494947, 13.479381)  # Richard-Sorge-Straße 21
midpoint_bb = (52.5104661, 13.432039)  # midpoint between location A and Le Wagon Berlin
url_2 = maps_url_tomidpoint_bb(location_A, midpoint_bb)
print(url_2)
print("check the file named: function_main_testing.py for STREAMLIT code implementation")
#streamlit code
'''markdown_url_2 = f"[{url_2}]({url_2})" 
st.markdown(markdown_url_2, unsafe_allow_html=True)'''





# #testing midpoint
# print(midpoint('Richard-Sorge-Straße 21, Berlin, Germany', 'Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany'))
# midpoint_test = midpoint('Richard-Sorge-Straße 21, Berlin, Germany', 'Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany')
# midpoint_string = f'{midpoint_test[0]},{midpoint_test[1]}'


# print(get_directions_to_midpoint('Richard-Sorge-Straße 21, Berlin, Germany', 'Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany', midpoint_test, 'biking'))
# directions_to_midpoint = get_directions_to_midpoint('Richard-Sorge-Straße 21, Berlin, Germany', 'Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany', midpoint_test, 'walking')
# print("--------------1---first_tuple_directions")
# first_tuple_directions = directions_to_midpoint[0]
# print(first_tuple_directions)
# print("--------------1.b--direction1")
# direction1 = directions_to_midpoint[0][0]
# print(direction1)   

# # get maps link for one location and the midpoint

# start_lat = 52.5199888
# start_lng = 13.4477593
# end_lat = 52.5195224
# end_lng = 13.4480721

# link = f"https://www.google.com/maps/dir/{start_lat},{start_lng}/{end_lat},{end_lng}"
# print(link)


# # get maps link for one location and the midpoint

# midpoint[0]
# midpoint[1]

# start_lat = 52.494947 #lat for location A Richard-Sorge-Straße 21, Berlin, Germany
# start_lng = 13.479381 # lng for lcoation A Richard-Sorge-Straße 21, Berlin, Germany
# midpoint_lat = 52.5104661 # midpoint lat between location A and location B Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany
# midpoint_lng = 13.432039 # midpoint lng between location A and location B Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany

# link = f"https://www.google.com/maps/dir/{start_lat},{start_lng}/{midpoint_lat},{midpoint_lng}"
# print(link)


# start_lat = 52.494947 #lat for location A Richard-Sorge-Straße 21, Berlin, Germany
# start_lng = 13.479381 # lng for lcoation A Richard-Sorge-Straße 21, Berlin, Germany
# midpoint_lat = midpoint[0] # midpoint lat between location A and location B Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany
# midpoint_lng = midpoint[1] # midpoint lng between location A and location B Le Wagon Berlin - Coding Bootcamp, Rudi-Dutschke-Straße, Berlin, Germany
