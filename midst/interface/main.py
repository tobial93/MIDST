import googlemaps
import requests
import json
from midst.params import *


def get_lat_lon(address: str, API_KEY): # for STREAMLIT DEPLOYMENT we are passing API_KEY
    '''
    Returns the long and lat of an imputed address
    '''
    gmaps = googlemaps.Client(key=API_KEY)

    geocode_result_1 = gmaps.geocode(address)

    lat_long_dict_1 = geocode_result_1[0]['geometry']['location']
    return lat_long_dict_1["lat"], lat_long_dict_1["lng"]

def midpoint(loc_1, loc_2):
    '''
    Returns a tuple with latitude and longitude from
    mid point between the two locations as tuple(lat&lon)
    loc_1: (lat, lon)
    '''
    return ((loc_1[0] + loc_2[0]) / 2, (loc_1[1] + loc_2[1]) / 2)

def time_to_get_there(address_1:str, address_2:str, midpoint:tuple, mode:str, API_KEY):
    '''
    Returns a tuple of the aproximate time to get to midpoint,
    when using specified transport mode, first elemente will be duration
    from address 1, second element in the touple will be duration
    from address 2
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

    # Parameters Person 2str
    params2 = {"origin": address_2,
              "destination": midpoint_string,
              "mode": mode,
              "key": API_KEY,
              }
    # API request for person 1
    res1 = requests.get(url, params=params1)
    route1 = json.loads(res1.content)["routes"][0]["legs"][0]
    # Distance and duration for person 1
    duration1 = route1["duration"]["text"]

    # API request for person 2
    res2 = requests.get(url, params=params2)
    route2 = json.loads(res2.content)["routes"][0]["legs"][0]
    # Distance and duration for person 2
    duration2 = route2["duration"]["text"]

    return duration1, duration2

def places(lat_long:tuple, radius:int, type:str, API_KEY):

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
    Returns a list of lists that incluides the latitude,
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

def maps_url_tomidpoint(location:tuple, midpoint:tuple):
    '''
    Returns a clickable hyperlink to Google Maps.
    The starting point is the location A lat/lng.
    The destination point is the midpoint lat/lng.
    '''
    start_lat, start_lng = location
    midpoint_lat, midpoint_lng = midpoint

    maps_url_tomidpoint = f"https://www.google.com/maps/dir/{start_lat},{start_lng}/{midpoint_lat},{midpoint_lng}"
    return maps_url_tomidpoint

def get_directions_to_midpoint_two_modes(loc_1, loc_2, mid_point, mode1, mode2, API_KEY):
    # Convert midpoint tuple to a string
    midpoint_string = f'{mid_point[0]},{mid_point[1]}'

    # Base URL for API
    url = "https://maps.googleapis.com/maps/api/directions/json?"

    # Parameters Person 1
    params1 = {"origin": f'{loc_1[0]},{loc_1[1]}',
              "destination": midpoint_string,
              "mode": mode1,
              "key": API_KEY,
              }

    # Parameters Person 2
    params2 = {"origin": f'{loc_2[0]},{loc_2[1]}',
              "destination": midpoint_string,
              "mode": mode2,
              "key": API_KEY,
              }

    # API request for person 1
    res1 = requests.get(url, params=params1)
    route1 = json.loads(res1.content)["routes"][0]["legs"][0]
    # Duration for person 1
    duration1_in_seconds = route1["duration"]["value"]

    # API request for person 2
    res2 = requests.get(url, params=params2)
    route2 = json.loads(res2.content)["routes"][0]["legs"][0]
    # Duration for person 2
    duration2_in_seconds = route2["duration"]["value"]

    # Convert adjusted duration to minutes
    duration1 = int(duration1_in_seconds)
    duration2 = int(duration2_in_seconds)
    return duration1, duration2

def find_true_midpoint(loc1, loc2, initial_midpoint, mode1, mode2, API_KEY, counter=0):
    """
    Returns an adjusted midpoint towards the location with the bigger travel time in
    the form of tuple with lat & lng
    """

    # initial_midpoint: latitude and longitude of the initial midpoint calculated by average
    if counter >= 10: # counter: number of recursive calls made so far
        return initial_midpoint

    # calculate travel time for person 1 to midpoint
    # calculate travel time for person 2 to midpoint
    travel1, travel2 = get_directions_to_midpoint_two_modes(loc1, loc2, initial_midpoint, mode1, mode2, API_KEY)

    # check if travel times are within 5 minutes of each other
    # if the travel times are within the threshold, the initial midpoint will be returned
    # if the travel times differ by more than 5 minutes, it will continue to change the midpoint
    # threshold of 5 minutes
    if abs(travel1 - travel2) < 300: # 300 seconds = 5 minutes
        return initial_midpoint

    # compare travel times
    # if travel 1 is larger than travel 2, a new midpoint is calculated between location 1 and the inital midpoint
    if travel1 > travel2:
        # change midpoint
        new_midpoint = midpoint(loc1, initial_midpoint)
        # call function with new midpoint and increment counter
        return find_true_midpoint(loc1, loc2, new_midpoint, mode1, mode2, API_KEY, counter=counter+1)
    # compare travel times
    # if travel 1 is smaller than travel 2, a new midpoint is calculated between location 2 and the inital midpoint
    if travel1 < travel2:
        # change midpoint
        new_midpoint = midpoint(loc2, initial_midpoint)
        # call function with new midpoint and increment counter
        return find_true_midpoint(loc1, loc2, new_midpoint, mode1, mode2, API_KEY, counter=counter+1)
