import requests
import json
import googlemaps


api_key = "AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q"

mode = "train"  # This can be selected from the drop-down menu

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

# def get_directions(mode):
#     #Starting Points as inputs from User
#     person1_address = "Schwedstraße 16, Berlin, Germany"
#     person2_address = "Rudi-Dutschke-Straße 26, Berlin, Germany"

#     # Person 1
#     person1_data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&language=de&key={}".format(person1_address, api_key)).json()
#     person1_location = person1_data["results"][0]["geometry"]["location"]

#     # Person 2
#     person2_data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&language=de&key={}".format(person2_address, api_key)).json()
#     person2_location = person2_data["results"][0]["geometry"]["location"]

#     # Midpoint calculation 
#     midpoint = ((person1_location["lat"] + person2_location["lat"]) / 2, (person1_location["lng"] + person2_location["lng"]) / 2)
#     midpoint_string = f'{midpoint[0]},{midpoint[1]}'
    
#     # Base URL for API 
#     url = "https://maps.googleapis.com/maps/api/directions/json?"

#     # Parameters Person 1 
#     params1 = {"origin": person1_address,
#               "destination": midpoint_string,
#               "mode": mode,
#               "key": api_key,
#               }

#     # Parameters Person 2
#     params2 = {"origin": person2_address,
#               "destination": midpoint_string,
#               "mode": mode,
#               "key": api_key,
#               }
#     # API request for person 1
#     res1 = requests.get(url, params=params1)
#     route1 = json.loads(res1.content)["routes"][0]["legs"][0]
#     # Distance and duration for person 1 
#     distance1 = route1["distance"]["text"]
#     duration1 = route1["duration"]["text"]

#     # API request for person 2
#     res2 = requests.get(url, params=params2)
#     route2 = json.loads(res2.content)["routes"][0]["legs"][0]
#     # Distance and duration for person 2
#     distance2 = route2["distance"]["text"]
#     duration2 = route2["duration"]["text"]
    
#     directions = f"Directions from person 1: {route1['steps']}\nDirections from person 2: {route2['steps']}"
    
#     return directions, f"Time to get to midpoint: {duration1} for person 1, {duration2} for person 2"

# directions, time_to_midpoint = get_directions(mode)
# print(directions)
# print(time_to_midpoint)


def get_directions_to_midpoint(address_1, address_2, midpoint, mode):
    # Convert midpoint tuple to a string
    # midpoint_string = str(midpoint[0]) + "," + str(midpoint[1])
    midpoint_string = f'{midpoint[0]},{midpoint[1]}'
    # Base URL for API 
    url = "https://maps.googleapis.com/maps/api/directions/json?"

    # Parameters Person 1 
    params1 = {"origin": address_1,
              "destination": midpoint_string,
              "mode": mode,
              "key": api_key,
              }

    # Parameters Person 2
    params2 = {"origin": address_2,
              "destination": midpoint_string,
              "mode": mode,
              "key": api_key,
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



midpoint = midpoint(address_1, address_2)
directions, duration = get_directions_to_midpoint(address_1, address_2, midpoint, mode)

print(directions)
print(duration)
