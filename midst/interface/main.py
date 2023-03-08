import googlemaps
import requests
import json
from midst.params import *

def midpoint(address_1:str, address_2:str):
    '''
    Returns a tuple with latitude and longitude from
    mid point between the two addresses
    '''
    gmaps = googlemaps.Client(key=API_KEY)

    geocode_result_1 = gmaps.geocode(address_1)
    geocode_result_2 = gmaps.geocode(address_2)

    lat_long_dict_1 = geocode_result_1[0]['geometry']['location']
    lat_long_dict_2 = geocode_result_2[0]['geometry']['location']

    return ((lat_long_dict_1["lat"] + lat_long_dict_2["lat"]) / 2, (lat_long_dict_1["lng"] + lat_long_dict_2["lng"]) / 2)

def get_directions_to_midpoint(address_1:str, address_2:str, midpoint:tuple, mode:str):
    '''
    Returns a tuple, the first element in the tuple is the directions from
    the adresses to the midpoint, and the second element is the time
    it takes to get to the midpoint
    '''
    # Convert midpoint tuple to a string
    # midpoint_string = str(midpoint[0]) + "," + str(midpoint[1])
    midpoint_string = f'{midpoint[0]},{midpoint[1]}'
    # Base URL for API
    url = "https://maps.googleapis.com/maps/api/directions/json?"

    # Parameters Person 1
    params1 = {"origin": address_1,
              "destination": midpoint_string,
              "mode": mode,
              "key": API_KEY,
              }

    # Parameters Person 2
    params2 = {"origin": address_2,
              "destination": midpoint_string,
              "mode": mode,
              "key": API_KEY,
              }
    # API request for person 1
    res1 = requests.get(url, params=params1)
    route1 = json.loads(res1.content)["routes"][0]["legs"][0]
    # Distance and duration for person 1
    distance1 = route1["distance"]["text"]
    duration1 = route1["duration"]["text"]

    # API request for person 2
    res2 = requests.get(url, params=params2)
    route2 = json.loads(res2.content)["routes"][0]["legs"][0]
    # Distance and duration for person 2
    distance2 = route2["distance"]["text"]
    duration2 = route2["duration"]["text"]

    # Directions for both persons
    directions = f"Directions from person 1: {route1['steps']}\nDirections from person 2: {route2['steps']}"

    return directions, f"Time to get to midpoint: {duration1} for person 1, {duration2} for person 2"

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

def coords_name(JSON:dict) -> dict:
    '''
    Returns a list of list with the latitude and
    longitude and the name of the listed places on the JSON file
    '''
    nr_of_results = len(JSON['results'])
    places_list = []

    for n in range(nr_of_results):
        place = []
        name = JSON['results'][n]['name']
        lat= JSON['results'][n]['geometry']['location']['lat']
        lng= JSON['results'][n]['geometry']['location']['lng']
        place.append(lat)
        place.append(lng)
        place.append(name)
        places_list.append(place)

    return places_list
