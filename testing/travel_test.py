import requests
import json
import googlemaps
import math 
api_key = "AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q"

# TravelMode = driving, bicycling, transit(public transport), walking

mode1 = "walking"  # This can be selected from the drop-down menu
mode2 = "bicycling" # calculate weights based on the travel mode to adjust for different travel time

address_1 = "Schwedstraße 16, Berlin, Germany"
address_2 = "Rudi-Dutschke-Straße 26, Berlin, Germany"

def midpoint(address_1:str, address_2:str):
    '''
    Returns a tuple with latitude and longitude from
    mid point between the two addresses
    '''
    gmaps = googlemaps.Client(key=api_key)

    geocode_result_1 = gmaps.geocode(address_1)
    geocode_result_2 = gmaps.geocode(address_2)

    lat_long_dict_1 = geocode_result_1[0]['geometry']['location']
    lat_long_dict_2 = geocode_result_2[0]['geometry']['location']

    return ((lat_long_dict_1["lat"] + lat_long_dict_2["lat"]) / 2, (lat_long_dict_1["lng"] + lat_long_dict_2["lng"]) / 2)

def seconds_to_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes} minutes {seconds} seconds"

def duration_in_minutes(duration: int) -> int:
    """
    Converts a duration in seconds to minutes, rounded up to the nearest minute
    """
    return math.ceil(duration / 60)


def calculate_weight(mode: str) -> float:
    """
    Returns a weight for the given travel mode
    """
    if mode == "walking":
        return 1.0
    elif mode == "bicycling":
        return 1.5
    elif mode == "driving":
        return 2.0
    elif mode == "transit":
        return 3.0
    else:
        raise ValueError("Invalid travel mode")


def format_duration(duration: int) -> str:
    """
    Formats a duration in seconds as a string in the format "H hours M minutes"
    """
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    return f"{hours} hours {minutes} minutes"

midpoint1 = (52.5308755, 13.383247149999999)

def get_directions_to_midpoint_two_modes(address_1, address_2, midpoint, mode1, mode2):
    # Convert midpoint tuple to a string
    midpoint_string = f'{midpoint1[0]},{midpoint1[1]}'
    # Base URL for API 
    url = "https://maps.googleapis.com/maps/api/directions/json"

    # Parameters Person 1 
    params1 = {"origin": address_1,
              "destination": midpoint_string,
              "mode": mode1,
              "key": api_key,
              }

    # Parameters Person 2
    params2 = {"origin": address_2,
              "destination": midpoint_string,
              "mode": mode2,
              "key": api_key,
              }
    # API request for person 1
    res1 = requests.get(url, params=params1)
    route1 = json.loads(res1.content)["routes"][0]["legs"][0]
    # Distance and duration for person 1 
    distance1 = route1["distance"]["value"]
    duration1 = route1["duration"]["value"]

    # API request for person 2
    res2 = requests.get(url, params=params2)
    route2 = json.loads(res2.content)["routes"][0]["legs"][0]
    # Distance and duration for person 2
    distance2 = route2["distance"]["value"]
    duration2 = route2["duration"]["value"]
    
    # Directions for both persons
    directions = f"Directions from person 1: {route1['steps']}\nDirections from person 2: {route2['steps']}"
    
    # Convert distance to float and convert to kilometers
    distance1_km = float(distance1[:-3].replace(",", ""))
    distance2_km = float(distance2[:-3].replace(",", ""))
    
    # Convert duration to minutes
    duration1_minutes = duration_in_minutes(duration1)
    duration2_minutes = duration_in_minutes(duration2)
    
    # Calculate weights for the different travel modes to adjust the travel time accordingly
    weight1 = calculate_weight(distance1_km, duration1_minutes)
    weight2 = calculate_weight(distance2_km, duration2_minutes)
    
    # Adjust travel times based on weights
    adjusted_duration1 = duration1_minutes * weight1 / (weight1 + weight2)
    adjusted_duration2 = duration2_minutes * weight2 / (weight1 + weight2)
    
    # Convert adjusted durations back to formatted string
    adjusted_duration1_str = format_duration(adjusted_duration1)
    adjusted_duration2_str = format_duration(adjusted_duration2)
    
    # Distance for both persons
    distance = f"Distance from person 1: {distance1}\nDistance from person 2: {distance2}"
    
    return directions, f"Time to get to midpoint: {adjusted_duration1_str} for person 1, {adjusted_duration2_str} for person 2", distance

directions, duration, distance = get_directions_to_midpoint_two_modes(address_1, address_2, midpoint, mode1, mode2)
print(directions)
print(duration)
print(distance)
