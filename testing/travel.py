import requests
import json
import googlemaps

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

def get_directions_to_midpoint_two_modes(address_1, address_2, midpoint, mode1, mode2):
    # Convert midpoint tuple to a string
    midpoint_string = f'{midpoint[0]},{midpoint[1]}'

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

    # Calculate weights based on the average time it takes for each mode to travel the same distance
    # Here, we assume that the distance for both persons is the same
    weights = { "driving": 1, "bicycling": duration2 / duration1, "transit": duration2 / duration1, "walking": duration2 / duration1 }

    # Calculate adjusted durations for person 1
    adjusted_durations1 = { mode: int(duration1 * weights[mode]) for mode in weights }

    # Directions for both persons
    directions = f"Directions from person 1: {route1['steps']}\nDirections from person 2: {route2['steps']}"

    # Adjusted duration for person 2
    adjusted_durations2 = int(duration2 / weights[mode2])

    return directions, f"Time to get to midpoint: {adjusted_durations1[mode1]} for person 1, {adjusted_durations2} for person 2"


# def seconds_to_minutes(seconds):
#     minutes, seconds = divmod(seconds, 60)
#     return f"{minutes} minutes {seconds} seconds"

# midpoint = midpoint(address_1, address_2)
# directions, duration_in_seconds = get_directions_to_midpoint_two_modes(address_1, address_2, midpoint, mode1, mode2)

# duration_in_minutes = seconds_to_minutes(int(duration_in_seconds.split()[0]))
# print(duration_in_minutes)



midpoint = midpoint(address_1, address_2)
directions, duration = get_directions_to_midpoint_two_modes(address_1, address_2, midpoint, mode1, mode2)

print(directions)
print(duration)