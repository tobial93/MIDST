import requests
import json

# Google Maps API endpoint URL
url = "https://maps.googleapis.com/maps/api/directions/json?"

# API key
api_key = "AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q"

# Start location for party A
origin1 = "Schwedstraße 16, Berlin, Germany"

# Destination location for party A
destination1 = "Rudi-Dutschke-Straße 26, Berlin, Germany"

# Start time for party A (in seconds since midnight, January 1, 1970 UTC)
# start_time1 = 1646545200  # 2022-03-05T12:00:00+01:00

# Mode of transportation for party A
mode1 = "driving"

# Start location for party B
origin2 = "Bürknerstraße 11, Berlin, Germany"

# Destination location for party B
destination2 = "Rudi-Dutschke-Straße 26, Berlin, Germany"

# Start time for party B (in seconds since midnight, January 1, 1970 UTC)
# start_time2 = 1646548800  # 2022-03-05T13:00:00+01:00

# Mode of transportation for party B
mode2 = "driving"

# Get travel time and distance for party A
params1 = {
    "origin": origin1,
    "destination": destination1,
    "mode": mode1,
    # "departure_time": start_time1,
    "key": api_key,
}
res1 = requests.get(url, params=params1)
# print(f'res1: {res1.content}')
route1 = json.loads(res1.content)["routes"][0]["legs"][0]
distance1 = route1["distance"]["value"]
duration1 = route1["duration"]["value"]

# Get travel time and distance for party B
params2 = {
    "origin": origin2,
    "destination": destination2,
    "mode": mode2,
    # "departure_time": start_time2,
    "key": api_key,
}
res2 = requests.get(url, params=params2)
route2 = json.loads(res2.content)["routes"][0]["legs"][0]
distance2 = route2["distance"]["value"]
duration2 = route2["duration"]["value"]

# Calculate the midpoint based on the starting time and estimated travel time for each party
# midpoint_time = (start_time1 + duration1/2 + start_time2 + duration2/2) / 2
params_midpoint = {
    "origins": f"{origin1}|{origin2}",
    "destinations": f"{destination1}|{destination2}",
    "mode": "driving",
    # "arrival_time": int(midpoint_time),
    "key": api_key,
}
res_midpoint = requests.get(url, params=params_midpoint)
print(f'res_midpoint.content:{res_midpoint.content}')
midpoint = json.loads(res_midpoint.content)["destination_addresses"][0]
print(f'res_midpoint.content:{res_midpoint.content}')
print("Midpoint:", midpoint)
