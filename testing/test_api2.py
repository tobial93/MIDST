import requests
import json
from geopy.distance import distance
from datetime import datetime

# API endpoint URLs
url1 = "https://maps.googleapis.com/maps/api/geocode/json"
url2 = "https://maps.googleapis.com/maps/api/directions/json"

# API key
api_key = "YOUR_API_KEY"

# Addresses
address1 = "1600 Amphitheatre Parkway, Mountain View, CA"
address2 = "1 Infinite Loop, Cupertino, CA"

# Travel modes
mode1 = "driving"
mode2 = "walking"

# Send Geocoding API requests
params1 = {"address": address1, "key": api_key}
res1 = requests.get(url1, params=params1)
data1 = json.loads(res1.content)

params2 = {"address": address2, "key": api_key}
res2 = requests.get(url1, params=params2)
data2 = json.loads(res2.content)

# Extract latitude and longitude of the two addresses
lat1 = data1["results"][0]["geometry"]["location"]["lat"]
lng1 = data1["results"][0]["geometry"]["location"]["lng"]

lat2 = data2["results"][0]["geometry"]["location"]["lat"]
lng2 = data2["results"][0]["geometry"]["location"]["lng"]

# Send Directions API requests
params3 = {"origin": f"{lat1},{lng1}", "destination": f"{lat2},{lng2}", "mode": mode1, "key": api_key}
res3 = requests.get(url2, params=params3)
data3 = json.loads(res3.content)

params4 = {"origin": f"{lat1},{lng1}", "destination": f"{lat2},{lng2}", "mode": mode2, "key": api_key}
res4 = requests.get(url2, params=params4)
data4 = json.loads(res4.content)

# Extract distance and duration of the two travel modes
distance1 = data3["routes"][0]["legs"][0]["distance"]["value"]
duration1 = data3["routes"][0]["legs"][0]["duration"]["value"]

distance2 = data4["routes"][0]["legs"][0]["distance"]["value"]
duration2 = data4["routes"][0]["legs"][0]["duration"]["value"]

# Calculate midpoint
midpoint_latlng = ((lat1, lng1), (lat2, lng2))
midpoint = distance(midpoint_latlng[0], midpoint_latlng[1]).meters / 2.0

# Calculate velocities
velocity1 = distance1 / duration1
velocity2 = distance2 / duration2

# Calculate meeting time
meeting_time = datetime.utcfromtimestamp((midpoint / (velocity1 + velocity2)) + datetime.utcnow().timestamp())

# Print results
print("Midpoint:", midpoint, "meters")
print("Velocity (driving):", velocity1, "m/s")
print("Velocity (walking):", velocity2, "m/s")
print("Meeting time:", meeting_time)
