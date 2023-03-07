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

def places(lat_long:tuple, radius:int):
    '''
    Returns a JSON with a list of places arround a point
    specified by latitude and longitude imputed as a tuple
    in a certan radius from this point
    '''
    location = f'{lat_long[0]}%2C{lat_long[1]}'

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={API_KEY}"

    places_json = requests.get(url=url)

    return(places_json)
