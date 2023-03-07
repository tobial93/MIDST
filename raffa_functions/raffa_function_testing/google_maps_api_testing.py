#google_maps_api_testing.py

import googlemaps
from datetime import datetime

israel_api_key = 'AIzaSyAa7smWhdougw5OHY5ek13d4cf6AsZH4rM'
midst_api_key = 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q'
gmaps = googlemaps.Client(key=midst_api_key)

# Geocoding an address with GEOCODE function of gmpas API
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
print(geocode_result[0])

# Print out the list of keys in the first item of the geocoding result
print("----------geocoding result---------------")
for key in geocode_result[0].keys():
    print(key)
# output address_components, formatted_address, geometry, place_id, types

# Loop over the ADDRESS COMPONENT list and print out each element
print("----------address_components---------------")
for component in geocode_result[0]['address_components']:
    for key, value in component.items():        
        print(f"{key}: {value}")
    print() # Add a blank line between elements for readability

# Print FORMATTED ADDRESS
print("----------formatted_address---------------")
geocode_formatted_address = geocode_result[0]['formatted_address']
print(geocode_formatted_address)
#OUTPUT: Google Building 40, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA


# Loop over GEOMETRY print out each element
print("----------geometry---------------")
geocode_geometry = geocode_result[0]['geometry']
print(geocode_geometry)

print("----------geometry KEYS AND SUBKEYS---------------")
for key, value in geocode_result[0]['geometry'].items():
    if isinstance(value, dict):
        print(f"{key}:")
        for subkey, subvalue in value.items():
            print(f"\t{subkey}: {subvalue}")
    else:
        print(f"{key}: {value}")

# GEOMETRY LAT & LONG
print("----------geometry LAT LON----------")
geocode_latitude = geocode_result[0]['geometry']['location']['lat']
geocode_longitude = geocode_result[0]['geometry']['location']['lng']

print(f"latitude: {geocode_latitude}")
print(f"longitude: {geocode_longitude}")

# Print PLACE ID
print("----------place_id----------")
geocode_place_id = geocode_result[0]['place_id']
print(geocode_place_id)


# Print TYPES
print("types---------------")
geocode_types = geocode_result[0]['types']
print(geocode_result[0]['types'])
