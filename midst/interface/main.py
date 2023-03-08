import googlemaps
import requests
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

def places_lat_long(JSON:dict, nr_results:int) -> dict:
    '''
    Returns a simple dictionary with only the latitude and
    longitude of the listed places on the JSON file
    '''
    nr_of_results = len(JSON['results'])
    places_dict = {}

    if nr_of_results >= nr_results:
        nr_of_results = nr_results
    for n in range(nr_of_results):
        name = JSON['results'][n]['name']
        lat_long = JSON['results'][n]['geometry']['location']
        places_dict[f'{name}'] = lat_long

    return places_dict
