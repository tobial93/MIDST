#google_places_api_testing.py

import requests

israel_api_key = 'AIzaSyAa7smWhdougw5OHY5ek13d4cf6AsZH4rM'
midst_api_key = 'AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q'
#gmaps = googlemaps.Client(key=midst_api_key)


#EXAMPLE 1
# The following example shows a Find Place request for "Museum of Contemporary Art Australia", including the photos, formatted_address, name, rating, opening_hours, and geometry fields:
input_text = "Museum of Contemporary Art Australia"
# formatted_address = 
# name = 
# rating = 
# opening_hours = 
# geometry =

url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key={midst_api_key}"

payload={"input": input_text}
headers = {}

response = requests.request("GET", url, headers=headers, params=payload)

print(response.text)


#EXAMPLE 2
# The following example shows a Find Place request for "Museum", including the photos, formatted_address, name, rating, opening_hours, and geometry fields:
input_text = "Museum"
# formatted_address = 
# name = 
# rating = 
# opening_hours = 
# geometry =

url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key={midst_api_key}"

payload={"input": input_text}
headers = {}

response = requests.request("GET", url, headers=headers, params=payload)

print(response.text)



#-----------------testing API PLACES TYPES

#import requests

# Define the API endpoint
endpoint = "https://maps.googleapis.com/maps/api/place/autocomplete/json"

# Define the API parameters
params = {
    "input": "restaurant",  # Your search query
    "types": "(cities)",  # Your preferred place type(s)
    "key": midst_api_key,  # Your Google API key
}

# Make a request to the API endpoint with the parameters
response = requests.get(endpoint, params=params)

# Get the suggestions from the API response
suggestions = [result["description"] for result in response.json()["predictions"]]

# Print the suggestions
print(suggestions)