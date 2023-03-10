import requests
import json
import googlemaps

api_key = "AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q"

# TravelMode = driving, bicycling, transit(public transport), walking

mode1 = "walking"  # This can be selected from the drop-down menu
mode2 = "transit" # calculate weights based on the travel mode to adjust for different travel time

address_1 = "Schwedstraße 16, Berlin, Germany"
address_2 = "Friedelstarße 52, Berlin, Germany"

def get_lat_lon(address: str):
    gmaps = googlemaps.Client(key=api_key)

    geocode_result_1 = gmaps.geocode(address)

    lat_long_dict_1 = geocode_result_1[0]['geometry']['location']
    return lat_long_dict_1["lat"], lat_long_dict_1["lng"]

def mid_point(loc_1, loc_2):
    '''
    Returns a tuple with latitude and longitude from
    mid point between the two locations as tuple(lat&lon)
    loc_1: (lat, lon)
    '''
    return ((loc_1[0] + loc_2[0]) / 2, (loc_1[1] + loc_2[1]) / 2)

def seconds_to_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes} minutes {seconds} seconds"

def get_directions_to_midpoint_two_modes(loc_1, loc_2, mid_point, mode1, mode2):
    # Convert midpoint tuple to a string
    midpoint_string = f'{mid_point[0]},{mid_point[1]}'

    # Base URL for API
    url = "https://maps.googleapis.com/maps/api/directions/json?"

    # Parameters Person 1
    params1 = {"origin": f'{loc_1[0]},{loc_1[1]}',
              "destination": midpoint_string,
              "mode": mode1,
              "key": api_key,
              }

    # Parameters Person 2
    params2 = {"origin": f'{loc_2[0]},{loc_2[1]}',
              "destination": midpoint_string,
              "mode": mode2,
              "key": api_key,
              }

    # API request for person 1
    res1 = requests.get(url, params=params1)
    # print(res1)
    route1 = json.loads(res1.content)["routes"][0]["legs"][0]
    # Distance and duration for person 1
    distance1 = route1["distance"]["text"]
    duration1_in_seconds = route1["duration"]["value"]

    # API request for person 2
    res2 = requests.get(url, params=params2)
    route2 = json.loads(res2.content)["routes"][0]["legs"][0]
    # Distance and duration for person 2
    distance2 = route2["distance"]["text"]
    duration2_in_seconds = route2["duration"]["value"]

    # # Calculate weights based on travel mode
    # if mode1 == "walking":
    #     weight1 = 1.0
    # elif mode1 == "bicycling":
    #     weight1 = 0.9
    # elif mode1 == "transit":
    #     weight1 = 0.7
    # elif mode1 == "driving":
    #     weight1 = 1.2

    # if mode2 == "walking":
    #     weight2 = 1.0
    # elif mode2 == "bicycling":
    #     weight2 = 0.9
    # elif mode2 == "transit":
    #     weight2 = 0.7
    # elif mode2 == "driving":
    #     weight2 = 1.2

    # # Calculate adjusted duration based on weights
    # total_weight = weight1 + weight2
    # adjusted_duration1 = duration1_in_seconds * (weight2 / total_weight)
    # adjusted_duration2 = duration2_in_seconds * (weight1 / total_weight)

    # Convert adjusted duration to minutes
    duration1 = int(duration1_in_seconds)
    duration2 = int(duration2_in_seconds)
    return duration1, duration2

    # Directions for both persons
    directions = f"Directions from person 1: {route1['steps']}\nDirections from person 2: {route2['steps']}"

    # Distance for both persons
    distance = f"Distance from person 1: {distance1}\nDistance from person 2: {distance2}"

    return directions, f"Time to get to midpoint: {duration1} for person 1, {duration2} for person 2", distance


# Test the updated function
#midpoint = midpoint(get_lat_lon(address_1), get_lat_lon(address_2))
#duration, distance = get_directions_to_midpoint_two_modes(address_1, address_2, midpoint, mode1, mode2)

# #print(directions)
# print(duration)
# print(distance)
# print(get_lat_lon(address_1), get_lat_lon(address_2))
