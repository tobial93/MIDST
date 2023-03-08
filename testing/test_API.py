import midst.interface.main as mdt
from midst.params import *
import pandas as pd


address_1 = 'Brandenburger Tor, Pariser Platz, Berlin'
address_2 = 'Berliner Dom, Am Lustgarten, Berlin'
type_ = 'restaurant'
mode = 'bike'

mid_point = mdt.midpoint(address_1=address_1, address_2=address_2)
JSON_places = mdt.places(mid_point,500,type_).json()
list_loc = mdt.coords_name(JSON_places)
directions = mdt.get_directions_to_midpoint(address_1, address_2, mid_point, mode)

coordinates_list = []
for n in range(len(list_loc)):
    cords = []
    cords.append(list_loc[0][0])
    cords.append(list_loc[0][1])
    coordinates_list.append(cords)

mid_point_df = pd.DataFrame(data=[mid_point], columns= ['lon', 'lat'])

print(mid_point_df)

# https://maps.googleapis.com/maps/api/staticmap?size=512x512&maptype=roadmap\
# &markers=size:mid%7Ccolor:red%7CSan+Francisco,CA%7COakland,CA%7CSan+Jose,CA&key={API_KEY}

# https://maps.googleapis.com/maps/api/staticmap?center=52.51589465,13.35198435&size=700x700&markers=color:red%7C52.51932469999999,13.3562407%7C52.5171076,13.34826%7C52.5171096,13.3482566&key=AIzaSyCfXloKda5Mcqpzlzr55RwWI3B_hkzsl4Q


# my_key = 'AIzaSyAa7smWhdougw5OHY5ek13d4cf6AsZH4rM'
# MIDST_key = API_KEY

# gmaps = googlemaps.Client(key=MIDST_key)

# # reverse_geocode_result = gmaps.reverse_geocode((52.5068689,13.3912953))

# geocode_result_1 = gmaps.geocode(address_1)
# geocode_result_2 = gmaps.geocode(address_2)

# lat_long_dict_1 = geocode_result_1[0]['geometry']['location']
# lat_long_dict_2 = geocode_result_2[0]['geometry']['location']

# midpoint = ((lat_long_dict_1["lat"] + lat_long_dict_2["lat"]) / 2, (lat_long_dict_1["lng"] + lat_long_dict_2["lng"]) / 2)

# radius = 500

# location = f'{midpoint[0]}%2C{midpoint[1]}'
# type_ = 'restaurant'
# keyword = 'chinese'

# url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type_}&keyword=cruise&key={MIDST_key}"

# response = requests.request("GET", url, headers=headers, data=payload)
