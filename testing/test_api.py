import requests
from geopy import distance
import json
import googlemaps
from datetime import datetime
import time
import os

# API Key
api_key = "AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q"
gmaps = googlemaps.Client(key='AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q')
geocode_result = gmaps.geocode('Schwedstraße 16, Berlin, Germany')
# print(f'geocode:{geocode_result}')
url = "https://maps.googleapis.com/maps/api/directions/json?"

# Time Stamp 
now = datetime.now()
# print(f'time stamp: {now}')
current_time = int(time.time() +(60*60)+ 10)
# print(datetime.utcfromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'))

# print(f'current time: {current_time}')

# Start time for party B (in seconds since midnight, January 1, 1970 UTC)
# start_time = datetime.now()
# print(f'time: {start_time}')

#Starting Points
person1_address = "Schwedstraße 16, Berlin, Germany"
person2_address = "Rudi-Dutschke-Straße 26, Berlin, Germany"

# Travel Mode
mode = "walking"

# Retrieve the geolocations of both people using the Google Maps API with a language key for Germany
# Person 1
person1_data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&language=de&key={}".format(person1_address, api_key)).json()
person1_location = person1_data["results"][0]["geometry"]["location"]
#print(f'person1_loc:{person1_location}')
# Person 2
person2_data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&language=de&key={}".format(person2_address, api_key)).json()
person2_location = person2_data["results"][0]["geometry"]["location"]
#print(f'person2_loc:{person2_location}')

# Midpoint based on the average lat and long of both parties
midpoint = ((person1_location["lat"] + person2_location["lat"]) / 2, (person1_location["lng"] + person2_location["lng"]) / 2)
print(f'midpoint:{midpoint}')

midpoint_dict = {"lat": midpoint[0], "lng": midpoint[1]}
midpoint1 = f'{midpoint[0]},{midpoint[1]}'
print(midpoint1)
url = "https://maps.googleapis.com/maps/api/directions/json?"
# Parameters Person 1 
params1 = {"origin": 'Schwedstraße 16, Berlin, Germany', # origin works with coordinates and address
          "destination": midpoint1,
          "mode": 'train',
          #"departure_time": current_time,
          "key": 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q',
          }
# Parameters Person 2
params2 = {"origin": 'Rudi-Dutschke-Straße 26, Berlin, Germany', # origin works with coordinates and address
          "destination": midpoint1,
          "mode": 'train',
          #"departure_time": current_time,
          "key": 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q',
          }
# API request for person 1
res1 = requests.get(url, params=params1)
# print(f'response:{res1}')
route1 = json.loads(res1.content)["routes"][0]["legs"][0]
# Distance and duration for person 1 
distance1 = route1["distance"]["text"]
duration1 = route1["duration"]["text"] # subtract both durations from each other --> if the difference is still in below the threshold --> continue
print(f'distance1:{distance1}')
print(f'duration1:{duration1}')
# API request for person 2
res2 = requests.get(url, params=params2)
route2 = json.loads(res1.content)["routes"][0]["legs"][0]
# Distance and duration for person 2
distance2 = route2["distance"]["text"]
duration2 = route2["duration"]["text"]
print(f'distance2:{distance2}')
print(f'duration2:{duration2}')

# midpoint_time = (current_time + duration1/2) 
# print(f'mipoint time: {midpoint_time}')

# params_midpoint = {
#     "origins": f"{person1_address}|{person2_address}",
#     "destinations": f"{midpoint}|{midpoint}",
#     "mode": mode,
#     "arrival_time": int(midpoint_time),
#     "key": api_key,
# }
# res_midpoint = requests.get(url, params=params_midpoint)
# print(f'res_midpoint.content:{res_midpoint.content}')

# response = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin={},{}&destination={}&mode={}&key={}".format(person1_address[0], person1_address[1],midpoint, mode, api_key)).json()
# print(f'response:{response}')

# API call works with all parameters for person 1
response1 = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin=52.5547798,13.37502&destination=52.5308755,13.383247149999999&mode=walking&key=AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q").json()
# print(f'response1:{response1}')

# API call works with all parameters for person 2
response2 = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin=52.5069712,13.3914743&destination=52.5308755,13.383247149999999&mode=walking&key=AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q").json()
# print(f'response2:{response2}')
midpoint = ((person1_location["lat"] + person2_location["lat"]) / 2, (person1_location["lng"] + person2_location["lng"]) / 2)
print(f'midpoint:{midpoint}')

# distance_km = distance.distance((person1_location["lat"], person1_location["lng"]), (person2_location["lat"], person2_location["lng"])).km
# print(f'distance_km:{distance_km}')
# time = distance_km / 1000 
# print(f'time:{time}')
# velocity_person1 = distance_km / (2 * time)
# velocity_person2 = distance_km / (2 * time) # velocity doesn't make sense --> find another way to calculate while using an api

print("Midpoint: {}".format(midpoint))
# print("Velocity for person 1: {:.2f} km/h".format(velocity_person1))
# print("Velocity for person 2: {:.2f} km/h".format(velocity_person2))
