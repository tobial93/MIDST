import requests
from geopy import distance

api_key = "AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q"
person1_address = "Schwedstraße 16, Berlin, Germany"
person2_address = "Rudi-Dutschke-Straße 26, Berlin, Germany"

# Retrieve the geolocations of both people using the Google Maps API with a language key for Germany
person1_data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&language=de&key={}".format(person1_address, api_key)).json()
print(f'first_request:{person1_data}')
person1_location = person1_data["results"][0]["geometry"]["location"]
person2_data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&language=de&key={}".format(person2_address, api_key)).json()
person2_location = person2_data["results"][0]["geometry"]["location"]

# Calculate the midpoint and the velocity needed for each person to reach the midpoint at the same time
midpoint = ((person1_location["lat"] + person2_location["lat"]) / 2, (person1_location["lng"] + person2_location["lng"]) / 2)
print(f'midpoint:{midpoint}')
distance_km = distance.distance((person1_location["lat"], person1_location["lng"]), (person2_location["lat"], person2_location["lng"])).km
print(f'distance_km:{distance_km}')
time = distance_km / 1000 
print(f'time:{time}')
velocity_person1 = distance_km / (2 * time)
velocity_person2 = distance_km / (2 * time) # velocity doesn't make sense --> find another way to calculate while using an api

print("Midpoint: {}".format(midpoint))
print("Velocity for person 1: {:.2f} km/h".format(velocity_person1))
print("Velocity for person 2: {:.2f} km/h".format(velocity_person2))
