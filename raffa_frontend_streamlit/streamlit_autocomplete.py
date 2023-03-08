
from raffa_functions.autocomplete import *
import streamlit as st
import requests
from streamlit_searchbox import st_searchbox


# Create a title for the app
st.title("MIDST app")

# Create a header for the input section
st.header("Input Parameters")


#---------------Location Input 1------

# Add a label above the searchbox
st.write("Starting Point A:")
# pass search function to searchbox
selected_location_A = st_searchbox(
    search_location_A, # test in the streamlit frontend>> 'Nordhauser Straße' >> select: address_1 = 'Nordhauser Straße 2, 10589 Berlin, Deutschland'
    key="location_searchbox_A",
)

#---------------Location Input 2------

# Add a label above the searchbox
st.write("Starting Point B:")
# pass search function to searchbox
if selected_location_A:
   
    selected_location_B = st_searchbox(
        search_location_B, # test in the streamlit frontend>> 'Rudi-Dutschke' >> select: address_2 = 'Rudi-Dutschke-Straße 26, 10969 Berlin'
        key="location_searchbox_B",
    )


# ACTIVITY TYPE component:
# Define options for the dropdown
dropdown_options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

# Create the searchbox with the dropdown
searchbox_value = st.selectbox("Select an option:", dropdown_options)
#searchbox_query = st.text_input("Search", "")

# # Display the searchbox values
# st.write("Selected option:", searchbox_value)
# st.write("Search query:", searchbox_query)

#---------------BUTTON------
#Add a button to submit the form
if st.button("Submit"):
     # Use the selected location for further processing
     st.write(f"You selected {selected_location_A}.")
     st.write(f"You selected {selected_location_B}.")



# #----------both-------
# # pass search function to searchbox for location A
# selected_location_A = st_searchbox(
#     search_location_both,
#     key="location_searchbox_A",
#     label="Starting Point A"
# )

# # pass search function to searchbox for location B
# selected_location_B = st_searchbox(
#     search_location_both,
#     key="location_searchbox_B",
#     label="Starting Point B"
# )